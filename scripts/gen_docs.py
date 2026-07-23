#!/usr/bin/env python3
"""Generate docs/en + docs/vi API reference markdown from the endpoint spec + manifest."""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(".")
SPEC = {e["path"]: e for e in json.load(open("scripts/data/endpoints.json", encoding="utf-8"))["endpoints"]}
MANIFEST = json.load(open("tests/data/endpoints_manifest.json", encoding="utf-8"))

MODULE_TITLE = {
    "instance": ("Instance Management", "Quản lý phiên bản (Instance)"),
    "apps": ("Application Management", "Quản lý ứng dụng"),
    "tasks": ("Task Management", "Quản lý tác vụ"),
    "phone": ("Cloud Phone Management", "Quản lý Cloud Phone"),
    "storage": ("Cloud Space / Storage", "Cloud Space / Lưu trữ"),
    "static_proxy": ("Static Residential Proxy", "Proxy dân cư tĩnh"),
    "dynamic_proxy": ("Dynamic Proxy", "Proxy động"),
    "email": ("Email Verification Service", "Dịch vụ xác minh Email"),
    "automation": ("Flow Automation (RPA)", "Tự động hóa luồng (RPA)"),
    "token": ("SDK Token", "SDK Token"),
    "touch": ("Touch Simulation", "Mô phỏng cảm ứng"),
}

L = {
    "en": {
        "ref": "API Reference", "methods": "Methods", "sig": "Signature", "params": "Parameters",
        "name": "Python argument", "api": "API name", "type": "Type", "req": "Required", "desc": "Description",
        "yes": "yes", "no": "no", "returns": "Returns", "returns_txt": "the response `data` field (raises `VMOSAPIError` when `code != 200`).",
        "example": "Example", "none": "This endpoint takes no parameters (besides optional `**extra`).",
        "nested": "Nested fields of", "back": "Back to index", "endpoint": "Endpoint",
        "note": "> Auto-generated from the [official VMOS Cloud OpenAPI documentation](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Parameter descriptions come from the official docs.",
        "index_title": "VMOS SDK — API Reference (English)",
        "index_intro": "Every namespace below is an attribute of `VMOSClient` / `AsyncVMOSClient` (e.g. `client.instance`). Async usage is identical — just `await` the same methods.",
        "module": "Module", "count": "Endpoints", "descr": "Description",
    },
    "vi": {
        "ref": "Tài liệu API", "methods": "Danh sách phương thức", "sig": "Chữ ký hàm", "params": "Tham số",
        "name": "Tham số Python", "api": "Tên trong API", "type": "Kiểu", "req": "Bắt buộc", "desc": "Mô tả",
        "yes": "có", "no": "không", "returns": "Trả về", "returns_txt": "trường `data` của phản hồi (ném `VMOSAPIError` khi `code != 200`).",
        "example": "Ví dụ", "none": "Endpoint này không nhận tham số (ngoài `**extra` tùy chọn).",
        "nested": "Các trường con của", "back": "Về trang chính", "endpoint": "Endpoint",
        "note": "> Được sinh tự động từ [tài liệu chính thức VMOS Cloud OpenAPI](https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html). Mô tả tham số giữ nguyên tiếng Anh theo tài liệu gốc.",
        "index_title": "VMOS SDK — Tài liệu API (Tiếng Việt)",
        "index_intro": "Mỗi namespace bên dưới là một thuộc tính của `VMOSClient` / `AsyncVMOSClient` (ví dụ `client.instance`). Dùng async giống hệt — chỉ cần `await` cùng phương thức.",
        "module": "Module", "count": "Số endpoint", "descr": "Mô tả",
    },
}

MODULE_DESC = {
    "instance": ("Restart/reset, properties, SIM/GPS/WiFi, ADB & shell commands, screenshots, previews, image upgrades, one-click new device, root switching, network tools, media injection.",
                  "Khởi động lại/reset, thuộc tính, SIM/GPS/WiFi, lệnh ADB & shell, chụp màn hình, xem trước, nâng cấp image, đổi máy một chạm, bật/tắt root, công cụ mạng, chèn media."),
    "apps": ("Install/uninstall, start/stop/restart apps, list installed apps, keep-alive and hidden-app lists.",
             "Cài/gỡ, khởi chạy/dừng/khởi động lại ứng dụng, liệt kê ứng dụng, giữ ứng dụng chạy nền và ẩn ứng dụng."),
    "tasks": ("Query status & details of asynchronous tasks (instance ops, file pushes).",
              "Truy vấn trạng thái & chi tiết các tác vụ bất đồng bộ (thao tác instance, đẩy file)."),
    "phone": ("Goods, orders, renewals, activation codes, authorization/transfer, backups, sharing, replacement.",
              "Gói dịch vụ, đơn hàng, gia hạn, mã kích hoạt, ủy quyền/chuyển giao, sao lưu, chia sẻ, thay thế thiết bị."),
    "storage": ("Storage goods, cloud-space backups, file upload/query/delete, storage renewal.",
                "Gói lưu trữ, sao lưu cloud space, tải lên/truy vấn/xóa file, gia hạn lưu trữ."),
    "static_proxy": ("Static residential IP goods, orders, proxy create/renew/manage.",
                     "Gói IP dân cư tĩnh, đơn hàng, tạo/gia hạn/quản lý proxy."),
    "dynamic_proxy": ("Dynamic proxy regions, goods, orders, traffic balance, per-pad proxy config.",
                      "Khu vực proxy động, gói, đơn hàng, số dư lưu lượng, cấu hình proxy cho từng máy."),
    "email": ("Email types & stock, purchase orders, verification-code retrieval.",
              "Loại email & tồn kho, đơn mua, lấy mã xác minh."),
    "automation": ("RPA flow scripts, task dispatch & scheduling, account matrix, webview, unmanned live.",
                   "Kịch bản RPA, điều phối & lập lịch tác vụ, ma trận tài khoản, webview, livestream không người trực."),
    "token": ("Issue & clear temporary STS tokens for the client-side SDK.",
              "Cấp & xóa token STS tạm thời cho SDK phía client."),
    "touch": ("Humanized click/swipe/long-press trajectories and raw multi-point touch.",
              "Quỹ đạo chạm/vuốt/nhấn giữ giống người thật và cảm ứng đa điểm mức thấp."),
}


def esc_md(s):
    return re.sub(r"\s+", " ", (s or "")).replace("|", "\\|").strip()


def sig_of(entry):
    req = [p for p in entry["params"] if p["required"] and not p["is_file"]]
    fil = [p for p in entry["params"] if p["is_file"]]
    opt = [p for p in entry["params"] if not p["required"] and not p["is_file"]]
    parts = [p["py"] for p in req] + [p["py"] for p in fil]
    if opt:
        parts.append("*")
        parts += [f"{p['py']}=None" for p in opt]
    parts.append("**extra")
    return f"client.{entry['module']}.{entry['method']}({', '.join(parts)})"


def param_rows(spec_ep, entry, lang):
    t = L[lang]
    by_api = {p["api"]: p for p in entry["params"]}
    lines = [f"| {t['name']} | {t['api']} | {t['type']} | {t['req']} | {t['desc']} |",
             "|---|---|---|---|---|"]
    for sp in spec_ep["params"]:
        mp = by_api.get(sp["name"])
        if not mp:
            continue
        req = t["yes"] if mp["required"] else t["no"]
        lines.append(f"| `{mp['py']}` | `{sp['name']}` | {esc_md(sp.get('type') or '-')} | {req} | {esc_md(sp.get('desc') or '')} |")
    nested = []
    for sp in spec_ep["params"]:
        if sp.get("children"):
            rows = [f"**{L[lang]['nested']} `{sp['name']}`:**", "",
                    f"| {t['api']} | {t['type']} | {t['desc']} |", "|---|---|---|"]
            for c in sp["children"]:
                rows.append(f"| `{esc_md(c['name'])}` | {esc_md(c.get('type') or '-')} | {esc_md(c.get('desc') or '')} |")
            nested.append("\n".join(rows))
    return "\n".join(lines), nested


def render_endpoint(path, entry, lang):
    t = L[lang]
    sp = SPEC[path]
    out = [f"### `{entry['method']}` — {esc_md(entry['name'])}", ""]
    if sp.get("description"):
        out += [esc_md(sp["description"])[:600], ""]
    out += [f"- **{t['endpoint']}**: `{entry['http_method']} {path}`", ""]
    out += [f"**{t['sig']}**", "", "```python", sig_of(entry), "```", ""]
    if entry["params"]:
        table, nested = param_rows(sp, entry, lang)
        out += [f"**{t['params']}**", "", table, ""]
        for n in nested:
            out += [n, ""]
    else:
        out += [t["none"], ""]
    ex = (sp.get("request_example") or "").strip()
    if ex and len(ex) < 1200 and entry["http_method"] != "GET" and not entry["params"].__len__() == 0:
        out += [f"**{t['example']}** (JSON payload)", "", "```json", ex, "```", ""]
    out += [f"**{t['returns']}**: {t['returns_txt']}", "", "---", ""]
    return "\n".join(out)


def main():
    by_module = defaultdict(list)
    for path, e in MANIFEST.items():
        by_module[e["module"]].append((path, e))

    for lang in ("en", "vi"):
        t = L[lang]
        outdir = ROOT / "docs" / lang
        outdir.mkdir(parents=True, exist_ok=True)
        index = [f"# {t['index_title']}", "", t["note"], "", t["index_intro"], "",
                 f"| {t['module']} | {t['count']} | {t['descr']} |", "|---|---|---|"]
        for mod in sorted(by_module):
            title = MODULE_TITLE[mod][0 if lang == "en" else 1]
            desc = MODULE_DESC[mod][0 if lang == "en" else 1]
            index.append(f"| [`client.{mod}`]({mod}.md) | {len(by_module[mod])} | {desc} |")
            page = [f"# `client.{mod}` — {title}", "", t["note"], "", desc, "",
                    f"## {t['methods']}", "",
                    "| Python | HTTP | Endpoint |", "|---|---|---|"]
            for path, e in by_module[mod]:
                page.append(f"| [`{e['method']}`](#{e['method'].replace('_','-')}--{re.sub(r'[^a-z0-9]+','-',e['name'].lower()).strip('-')}) | {e['http_method']} | `{path}` |")
            page += ["", f"[{t['back']}](README.md)", "", "---", ""]
            for path, e in by_module[mod]:
                page.append(render_endpoint(path, e, lang))
            (outdir / f"{mod}.md").write_text("\n".join(page), encoding="utf-8")
        total = sum(len(v) for v in by_module.values())
        if lang == "en":
            topics = ["[Cloud Real Device — changeable properties](real-device-properties.md)",
                      "[Device-Spoofing Toolkit (reseller)](device-spoofing-toolkit.md)"]
        else:
            topics = ["[Thiết bị thật — thuộc tính đổi được](thiet-bi-that-properties.md)",
                      "[Toolkit spoof thiết bị (reseller)](toolkit-spoof-thiet-bi.md)"]
        index += ["", "## " + ("Topic guides" if lang == "en" else "Hướng dẫn chuyên đề"), ""]
        index += ["- " + t for t in topics]
        index += [""]
        index += ["", f"**Total: {total} endpoints / 11 namespaces.**", ""]
        if lang == "en":
            index += ["See also: [../vi/README.md](../vi/README.md) — Tài liệu tiếng Việt.", ""]
        else:
            index += ["Xem thêm: [../en/README.md](../en/README.md) — English documentation.", ""]
        (outdir / "README.md").write_text("\n".join(index), encoding="utf-8")
        print(f"docs/{lang}: {len(by_module)} module pages")


if __name__ == "__main__":
    main()
