#!/usr/bin/env python3
"""Generate vmos SDK api modules from build/endpoints.json."""
import json
import keyword
import re
from collections import OrderedDict, defaultdict
from pathlib import Path

SPEC = json.load(open("scripts/data/endpoints.json", encoding="utf-8"))
OUT_DIR = Path("src/vmos/api")
MANIFEST_OUT = Path("tests/data/endpoints_manifest.json")

CATEGORY_MODULE = {
    "Instance Management": ("instance", "Instance"),
    "Resource Management": ("instance", "Instance"),
    "Application Management": ("apps", "Apps"),
    "Task Management": ("tasks", "Tasks"),
    "Cloud Phone Management": ("phone", "Phone"),
    "Cloud Space": ("storage", "Storage"),
    "Static Residential Service": ("static_proxy", "StaticProxy"),
    "Dynamic Proxy Service": ("dynamic_proxy", "DynamicProxy"),
    "Email Verification Service": ("email", "Email"),
    "Flow Automation (RPA)": ("automation", "Automation"),
    "SDK Token": ("token", "Token"),
    "Touch Simulation": ("touch", "Touch"),
}

MODULE_DOC = {
    "instance": "Instance management: restart/reset, properties, SIM/GPS/WiFi, ADB, screenshots, previews, image upgrade, one-click new device, root, network tools, media injection and more.",
    "apps": "Application management: install/uninstall, start/stop/restart apps, app lists, keep-alive and hidden-app configuration.",
    "tasks": "Task management: query the status and details of asynchronous instance/file tasks.",
    "phone": "Cloud phone commerce & lifecycle: goods, orders, renewal, activation codes, authorization/transfer, backups, device sharing and replacement.",
    "storage": "Cloud Space: storage goods, backups, file management (upload/query/delete) and renewal of cloud storage.",
    "static_proxy": "Static residential IP service: goods, orders, proxy creation/renewal and management.",
    "dynamic_proxy": "Dynamic proxy service: regions, goods, orders, traffic balance and per-pad proxy configuration.",
    "email": "Email verification service: email types/stock, purchase orders and verification-code retrieval.",
    "automation": "Flow Automation (RPA): flow script templates, task dispatch/scheduling, account matrix operations, webview and unmanned live streaming.",
    "token": "SDK temporary token issuance (STS) for client-side SDK authentication, and token clearing.",
    "touch": "Humanized touch simulation: click / swipe / long-press with human-like trajectories, plus raw multi-point touch.",
}

TOUCH = {"simulateClick", "simulateSwipe", "simulateLongPress", "simulateTouch"}
TASKS = {"padTaskDetail", "fileTaskDetail", "getTaskStatus", "padExecuteTaskInfo"}
NAME_OVERRIDES = {
    "/vcpcloud/api/vcEmailService/getEmailCode": "get_email_code_vc",
    "/vcpcloud/api/vcEmailService/getEmailOrder": "get_email_order_vc",
}


def snake(name: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = re.sub(r"_+", "_", s).strip("_").lower()
    if not s or not s[0].isalpha():
        s = "p_" + s
    if keyword.iskeyword(s):
        s += "_"
    return s


def module_for(ep) -> str:
    tail = ep["path"].rstrip("/").split("/")[-1]
    if tail in TOUCH:
        return "touch"
    if tail in TASKS:
        return "tasks"
    if "Email" in ep["path"] or "vcEmailService" in ep["path"]:
        return "email"
    mod, _ = CATEGORY_MODULE.get(ep["category"], ("instance", "Instance"))
    return mod


def method_name(ep, mod: str) -> str:
    if ep["path"] in NAME_OVERRIDES:
        return NAME_OVERRIDES[ep["path"]]
    parts = ep["path"].rstrip("/").split("/")
    try:
        i = parts.index("padApi")
        segs = parts[i + 1:]
    except ValueError:
        segs = parts[-1:]
    name = snake("_".join(segs))
    if mod == "automation" and name.startswith("automation_"):
        name = name[len("automation_"):]
    return name


def py_type(t: str) -> str:
    t = (t or "").lower().strip()
    if not t:
        return "Any"
    if "string[]" in t or "array[string]" in t or t == "list<string>":
        return "Sequence[str]"
    if "object[]" in t or "array[object]" in t or "jsonarray" in t:
        return "Sequence[Mapping[str, Any]]"
    if t.endswith("[]") or t.startswith("array") or t.startswith("list"):
        return "Sequence[Any]"
    if "string" in t or t in ("str",):
        return "str"
    if t in ("integer", "int", "long", "int64", "int32") or "integer" in t:
        return "int"
    if t in ("number", "float", "double", "bigdecimal"):
        return "float"
    if "bool" in t:
        return "bool"
    if "object" in t or "map" in t:
        return "Mapping[str, Any]"
    if t == "file":
        return "Any"
    return "Any"


def esc(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


def clip(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return (s[: n - 1] + "…") if len(s) > n else s


HEADER = '''"""{doc}

Auto-generated from the official VMOS Cloud OpenAPI documentation.
https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Every method returns the response ``data`` field and raises
:class:`vmos.exceptions.VMOSAPIError` when the API answers ``code != 200``.
Undocumented/new parameters can always be passed via ``**extra``.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from ._base import AsyncAPIResource, SyncAPIResource, build_payload

__all__ = ["{sync_cls}", "{async_cls}"]

'''


def build_method(ep, mname, is_async):
    http_method = ep["method"].upper()
    style = ep["param_style"]
    params = []
    seen = set()
    for p in ep["params"]:
        if not p["name"] or not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", p["name"].replace("-", "_")):
            continue
        pn = snake(p["name"])
        if pn in seen:
            continue
        seen.add(pn)
        params.append({
            "py": pn,
            "api": p["name"],
            "required": bool(p.get("required")),
            "type": py_type(p.get("type", "")),
            "desc": clip(p.get("desc", ""), 220),
            "children": [c["name"] for c in p.get("children", []) if c.get("name")],
            "is_file": (p.get("type", "").lower() == "file"),
        })
    req = [p for p in params if p["required"] and not p["is_file"]]
    opt = [p for p in params if not p["required"] and not p["is_file"]]
    fparams = [p for p in params if p["is_file"]]

    a = "async " if is_async else ""
    aw = "await " if is_async else ""
    sig = [f"    {a}def {mname}(", "        self,"]
    for p in req:
        sig.append(f"        {p['py']}: {p['type']},")
    if fparams:
        for p in fparams:
            sig.append(f"        {p['py']}: Any,")
    if opt:
        sig.append("        *,")
    for p in opt:
        sig.append(f"        {p['py']}: Optional[{p['type']}] = None,")
    sig.append("        **extra: Any,")
    sig.append("    ) -> Any:")

    # docstring
    d = [f'        """{esc(clip(ep["name"], 90))}.']
    desc = clip(ep.get("description", ""), 500)
    if desc:
        d.append("")
        d.append(f"        {desc}")
    d.append("")
    d.append(f"        ``{http_method} {ep['path']}``")
    if params:
        d.append("")
        d.append("        Args:")
        for p in req + fparams + opt:
            line = f"            {p['py']}: "
            bits = []
            if p["desc"]:
                bits.append(p["desc"])
            bits.append(f"(API: ``{p['api']}``" + (", required)" if p["required"] else ")"))
            if p["children"]:
                bits.append("Nested fields: " + ", ".join(f"``{c}``" for c in p["children"][:16]) + ".")
            d.append(line + " ".join(bits))
        d.append("            **extra: Extra parameters sent verbatim (forward compatibility).")
    d.append("")
    d.append("        Returns:")
    d.append("            The response ``data`` field.")
    d.append('        """')

    # body
    b = []
    named = ", ".join(f'"{p["api"]}": {p["py"]}' for p in req + opt)
    payload_expr = f"build_payload({{{named}}}, extra)" if named else "build_payload({}, extra)"
    if fparams:
        fp = fparams[0]
        b.append(f"        payload = {payload_expr}")
        b.append(f'        return {aw}self._client.request("{http_method}", "{ep["path"]}", json_body=payload, files={{"{fp["api"]}": {fp["py"]}}})')
    elif http_method == "GET":
        b.append(f"        payload = {payload_expr}")
        b.append(f'        return {aw}self._client.request("GET", "{ep["path"]}", query=payload)')
    else:
        b.append(f"        payload = {payload_expr}")
        b.append(f'        return {aw}self._client.request("{http_method}", "{ep["path"]}", json_body=payload)')
    return "\n".join(sig + d + b), params


def main():
    modules = defaultdict(list)
    for ep in SPEC["endpoints"]:
        modules[module_for(ep)].append(ep)

    manifest = OrderedDict()
    class_names = {}
    for mod, eps in sorted(modules.items()):
        cls_base = "".join(w.capitalize() for w in mod.split("_"))
        sync_cls, async_cls = f"{cls_base}API", f"Async{cls_base}API"
        class_names[mod] = (sync_cls, async_cls)
        # stable order: doc order
        used = set()
        methods_sync, methods_async = [], []
        for ep in eps:
            mname = method_name(ep, mod)
            base = mname
            n = 2
            while mname in used:
                mname = f"{base}_v{n}"
                n += 1
            used.add(mname)
            s_code, params = build_method(ep, mname, is_async=False)
            a_code, _ = build_method(ep, mname, is_async=True)
            methods_sync.append(s_code)
            methods_async.append(a_code)
            manifest[ep["path"]] = {
                "module": mod,
                "sync_class": sync_cls,
                "async_class": async_cls,
                "method": mname,
                "http_method": ep["method"].upper(),
                "param_style": ep["param_style"],
                "name": ep["name"],
                "category": ep["category"],
                "params": [
                    {"py": p["py"], "api": p["api"], "required": p["required"], "type": p["type"], "is_file": p["is_file"]}
                    for p in params
                ],
            }

        src = HEADER.format(doc=MODULE_DOC.get(mod, mod), sync_cls=sync_cls, async_cls=async_cls)
        src += f"\nclass {sync_cls}(SyncAPIResource):\n"
        src += f'    """{MODULE_DOC.get(mod, mod)}"""\n\n'
        src += "\n\n".join(methods_sync)
        src += f"\n\n\nclass {async_cls}(AsyncAPIResource):\n"
        src += f'    """Async variant of :class:`{sync_cls}`."""\n\n'
        src += "\n\n".join(methods_async)
        src += "\n"
        (OUT_DIR / f"{mod}.py").write_text(src, encoding="utf-8")

    # api/__init__.py
    lines = ['"""Generated VMOS API namespaces."""', "", "from __future__ import annotations", ""]
    for mod in sorted(modules):
        s, a = class_names[mod]
        lines.append(f"from .{mod} import {s}, {a}")
    lines.append("")
    lines.append("SYNC_NAMESPACES = {")
    for mod in sorted(modules):
        lines.append(f'    "{mod}": {class_names[mod][0]},')
    lines.append("}")
    lines.append("")
    lines.append("ASYNC_NAMESPACES = {")
    for mod in sorted(modules):
        lines.append(f'    "{mod}": {class_names[mod][1]},')
    lines.append("}")
    lines.append("")
    lines.append("__all__ = [")
    for mod in sorted(modules):
        s, a = class_names[mod]
        lines.append(f'    "{s}", "{a}",')
    lines.append('    "SYNC_NAMESPACES", "ASYNC_NAMESPACES",')
    lines.append("]")
    (OUT_DIR / "__init__.py").write_text("\n".join(lines) + "\n", encoding="utf-8")

    json.dump(manifest, open(MANIFEST_OUT, "w", encoding="utf-8"), indent=1)
    total = sum(len(v) for v in modules.values())
    print(f"generated {len(modules)} modules, {total} endpoints")
    for mod in sorted(modules):
        print(f"  {mod}: {len(modules[mod])}")


if __name__ == "__main__":
    main()
