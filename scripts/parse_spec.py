#!/usr/bin/env python3
"""Parse the VMOS OpenAPI markdown (Jina-rendered) into a machine-readable spec JSON."""
import json
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "OpenAPI.md"  # markdown dump of the official docs
OUT = "scripts/data/endpoints.json"

text = open(SRC, encoding="utf-8").read()
lines = text.split("\n")

# --- helpers -----------------------------------------------------------------
def clean_heading(h: str) -> str:
    # "#### [**Modify Instance WIFI Properties**](url)" -> "Modify Instance WIFI Properties"
    h = re.sub(r"^#+\s*", "", h).strip()
    m = re.match(r"\[(.+?)\]\(.*\)$", h)
    if m:
        h = m.group(1)
    h = h.strip("*").strip()
    h = re.sub(r"\s*\{#[^}]+\}\s*", "", h)  # strip {#anchor}
    h = re.sub(r"^\d+\.\s*", "", h)  # strip "1. "
    return h.strip()

REQ_TABLE_MARKERS = re.compile(
    r"^\*\*Request (BODY |Body |Query |form-data )?[Pp]arameters?:?\*\*$|^\*\*Request Body:?\*\*$|^\*\*Request parameters:?\*\*$"
)
RESP_TABLE_MARKER = re.compile(r"^\*\*Response [Pp]arameters?:?\*\*$|^\*\*Response\*\*$")
EP_MARKER = re.compile(r"^\*\*(API Endpoint|Endpoint URL|Endpoint|API Address:?|Interface Address)\*\*$")
METHOD_MARKER = re.compile(r"^\*\*(Request )?Method:?\*\*$")
CT_MARKER = re.compile(r"^\*\*(Request (Content.?Type|Data Type):?|Content-Type)\*\*$")
CT_INLINE = re.compile(r"^\*\*Content-Type\*\*:?\s*(.+)$")
METHOD_IN_PATH = re.compile(r"^(GET|POST|PUT|DELETE)\s+(/.*)$", re.I)
CAT_RE = re.compile(r"(Management|Service|Space|Token|RPA|Simulation)")
REQ_EX_MARKER = re.compile(r"^\*\*Request [Ee]xample.*\*\*$")
RESP_EX_MARKER = re.compile(r"^\*\*Response [Ee]xample.*\*\*$")

def parse_table(block_lines, start_idx):
    """Parse a markdown table starting at/after start_idx; return (rows, end_idx)."""
    i = start_idx
    # find first line starting with |
    while i < len(block_lines) and not block_lines[i].strip().startswith("|"):
        if block_lines[i].strip().startswith(("**", "####", "###")) and i > start_idx:
            return [], i
        i += 1
    rows = []
    while i < len(block_lines) and block_lines[i].strip().startswith("|"):
        cells = [c.strip() for c in block_lines[i].strip().strip("|").split("|")]
        rows.append(cells)
        i += 1
    return rows, i

def rows_to_params(rows, has_required=True):
    """Convert table rows to params using header-driven column mapping."""
    params = []
    if not rows:
        return params
    header = [c.lower().strip() for c in rows[0]]

    def col(*names):
        for n in names:
            for i, h in enumerate(header):
                if h == n:
                    return i
        for n in names:
            for i, h in enumerate(header):
                if n in h:
                    return i
        return None

    ci_name = col("parameter name", "parameter", "field", "name")
    ci_ex = col("example value", "example")
    ci_type = col("data type", "type")
    ci_req = col("required")
    ci_def = col("default")
    ci_desc = col("description", "explanation")
    if ci_name is None:
        ci_name = 0

    data_rows = [r for r in rows[1:] if not all(set(c) <= {"-", " ", ":"} for c in r)]
    current = None
    for r in data_rows:
        while len(r) < len(header):
            r.append("")
        def cell(i):
            return r[i].strip() if i is not None and i < len(r) else ""
        name_raw = cell(ci_name)
        is_nested = bool(re.match(r"^[├│└─\s]*[├└│]", name_raw))
        clean_name = re.sub(r"^[├│└─\s]+", "", name_raw).strip().strip("`")
        entry = {
            "name": clean_name,
            "example": cell(ci_ex),
            "type": cell(ci_type),
            "desc": cell(ci_desc),
            "raw_name": name_raw,
        }
        if ci_def is not None and cell(ci_def) not in ("", "-"):
            entry["default"] = cell(ci_def)
        if has_required:
            entry["required"] = cell(ci_req).lower() in ("yes", "true", "y", "required")
        if is_nested:
            if current is not None:
                current.setdefault("children", []).append(entry)
        else:
            params.append(entry)
            current = entry
    return params

# --- split into blocks by headings -------------------------------------------
heading_re = re.compile(r"^(#{2,4}) ")
blocks = []  # (level, heading_line_idx, start, end)
idxs = [i for i, l in enumerate(lines) if heading_re.match(l)]
for n, i in enumerate(idxs):
    end = idxs[n + 1] if n + 1 < len(idxs) else len(lines)
    level = len(lines[i].split(" ")[0])
    blocks.append((level, i, i + 1, end))

# --- overview tables: authoritative path -> category map ----------------------
overview_cat = {}
_cat = ""
for l in lines:
    if l.startswith("## ") and "OpenAPI Interface List" in l:
        break
    if l.startswith("### "):
        _cat = clean_heading(l)
        continue
    m = re.match(r"^\|\s*\[(/[^\]]+)\]", l.strip())
    if m and _cat:
        overview_cat[m.group(1).strip()] = _cat

endpoints = []
callbacks = []
current_h2 = ""
current_h3 = ""

for level, hi, start, end in blocks:
    heading = clean_heading(lines[hi])
    if level == 2:
        current_h2 = heading
        current_h3 = ""
        continue
    body = lines[start:end]
    body_text = "\n".join(body)
    has_ep_marker = any(EP_MARKER.match(l.strip()) for l in body)

    # callback blocks: under a Callback h2, have parameter tables but no API Endpoint
    if "Callback" in heading and not has_ep_marker:
        rows = None
        for j, l in enumerate(body):
            if l.strip().startswith("|"):
                rows, _ = parse_table(body, j)
                break
        desc_lines = []
        for l in body:
            if l.strip().startswith("|") or l.strip().startswith("```"):
                break
            if l.strip() and not l.strip().startswith("**"):
                desc_lines.append(l.strip())
        ex = re.search(r"```\n(.*?)```", body_text, re.S)
        callbacks.append({
            "name": heading,
            "description": " ".join(desc_lines)[:500],
            "params": rows_to_params(rows or [], has_required=False),
            "example": ex.group(1).strip() if ex else "",
        })
        continue

    if not has_ep_marker:
        if level == 3 and CAT_RE.search(heading):
            current_h3 = heading
        continue

    # --- endpoint block (may contain MULTIPLE endpoints) ---
    if "Touch Simulation" in current_h2 and not current_h3:
        cat = "Touch Simulation"
    else:
        cat = current_h3 or current_h2

    marker_idxs = [j for j, l in enumerate(body) if EP_MARKER.match(l.strip())]
    segments = []
    for si, mi in enumerate(marker_idxs):
        seg_start = 0 if si == 0 else marker_idxs[si - 1] + 1
        # description zone: text between previous segment's content end and this marker
        seg_end = marker_idxs[si + 1] if si + 1 < len(marker_idxs) else len(body)
        segments.append((seg_start, mi, seg_end))

    for si, (seg_start, mi, seg_end) in enumerate(segments):
        sub = body[mi:seg_end]          # from EP marker onward: path/method/tables/examples
        pre = body[seg_start:mi]        # text before marker: description zone

        def after_marker(marker, _body=sub):
            for j, l in enumerate(_body):
                if (marker.match(l.strip()) if isinstance(marker, re.Pattern) else l.strip() == marker):
                    for k in range(j + 1, min(j + 6, len(_body))):
                        s = _body[k].strip()
                        if s.startswith(">"):
                            return s.lstrip("> ").strip(), k
                        if s and not s.startswith(">"):
                            break
            return "", -1

        path, _ = after_marker(EP_MARKER)
        path = path.strip("`").strip()
        method_override = ""
        mp = METHOD_IN_PATH.match(path)
        if mp:
            method_override = mp.group(1).upper()
            path = mp.group(2).strip()
        if not path.startswith("/"):
            continue

        # name: heading for first segment, else derived from path tail
        if si == 0:
            ep_name = heading
        else:
            tail = path.rstrip("/").split("/")[-1]
            ep_name = re.sub(r"(?<!^)(?=[A-Z])", " ", tail).title()

        # description: last prose lines before the marker (skip code/tables)
        desc = []
        in_code = False
        for l in pre:
            s = l.strip()
            if s.startswith("```"):
                in_code = not in_code
                continue
            if in_code or not s:
                continue
            if s.startswith(("**", ">", "|", "!", "#")):
                desc = []
                continue
            desc.append(s)
        description = " ".join(desc).strip()

        ep = {"name": ep_name, "category_h2": current_h2, "category": cat,
              "description": description, "path": path}
        method, _ = after_marker(METHOD_MARKER)
        ep["method"] = (method_override or method or "POST").upper()
        ct, _ = after_marker(CT_MARKER)
        if not ct:
            for l in sub:
                mm = CT_INLINE.match(l.strip())
                if mm:
                    ct = mm.group(1).strip().strip("`")
                    break
        ep["content_type"] = ct or "application/json"
        if ep["path"] in overview_cat:
            ep["category"] = overview_cat[ep["path"]]

        ep["params"] = []
        ep["param_style"] = "query" if ep["method"] == "GET" else ("form" if "form" in ep["content_type"] else "json")
        for j, l in enumerate(sub):
            s = l.strip()
            if REQ_TABLE_MARKERS.match(s):
                if "form-data" in s:
                    ep["param_style"] = "form"
                rows, _ = parse_table(sub, j + 1)
                ps = rows_to_params(rows, has_required=True)
                if ps:
                    ep["params"].extend(ps)
        for j, l in enumerate(sub):
            if RESP_TABLE_MARKER.match(l.strip()):
                rows, _ = parse_table(sub, j + 1)
                ep["response_params"] = rows_to_params(rows, has_required=False)
                break

        def code_after(marker_re, _body=sub):
            for j, l in enumerate(_body):
                if marker_re.match(l.strip()):
                    m2 = re.search(r"```[a-zA-Z]*\n(.*?)```", "\n".join(_body[j:]), re.S)
                    if m2:
                        return m2.group(1).strip()
            return ""
        ep["request_example"] = code_after(REQ_EX_MARKER)
        ep["response_example"] = code_after(RESP_EX_MARKER)
        endpoints.append(ep)

# --- dedupe by path (keep richer doc, merge params) ---------------------------
by_path = {}
for ep in endpoints:
    key = ep["path"]
    if key not in by_path:
        by_path[key] = ep
    else:
        old = by_path[key]
        # merge params by name
        names = {p["name"] for p in old["params"]}
        for p in ep["params"]:
            if p["name"] not in names:
                old["params"].append(p)
        old.setdefault("variants", []).append({"name": ep["name"], "category": ep["category"], "description": ep["description"], "request_example": ep["request_example"]})

result = {"endpoints": list(by_path.values()), "callbacks": callbacks}
json.dump(result, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

cats = {}
for ep in by_path.values():
    cats.setdefault(ep["category"], []).append(ep["path"])
print(f"endpoints: {len(by_path)}  callbacks: {len(callbacks)}")
for c, paths in cats.items():
    print(f"  [{c}] {len(paths)}")
missing_method = [e["path"] for e in by_path.values() if e["method"] not in ("GET", "POST", "PUT")]
noparams = [e["path"] for e in by_path.values() if not e["params"]]
print("odd methods:", missing_method)
print(f"no-params endpoints ({len(noparams)}):", noparams[:20])
