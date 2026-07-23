"""Spec-driven verification of EVERY endpoint wrapper in the SDK.

For each of the endpoints in ``tests/data/endpoints_manifest.json`` (extracted
from the official VMOS OpenAPI docs) this test:

1. resolves the SDK method on the right client namespace,
2. calls it with synthesized arguments through a mock transport,
3. asserts the request hit the documented path with the documented HTTP method,
4. asserts every documented parameter was serialized under its exact API name,
5. re-computes the V2 signature over the exact bytes sent and asserts it
   matches the ``X-Sign`` header (GET -> query string, JSON -> raw body,
   multipart -> empty string).
"""

import json
from pathlib import Path

import httpx
import pytest

from vmos import VMOSClient
from vmos.auth import V2Signer

AK, SK = "test_ak", "test_sk"
MANIFEST = json.loads((Path(__file__).parent / "data" / "endpoints_manifest.json").read_text(encoding="utf-8"))


def sample_for(param):
    """Synthesize a plausible argument for a manifest parameter."""
    t = param["type"]
    if param.get("is_file"):
        return ("test.apk", b"\x00\x01\x02")
    if t == "Sequence[str]":
        return ["AC11111111111"]
    if t == "Sequence[Mapping[str, Any]]":
        return [{"k": "v"}]
    if t == "Sequence[Any]":
        return ["item"]
    if t == "str":
        return "sample"
    if t == "int":
        return 1
    if t == "float":
        return 1.5
    if t == "bool":
        return True
    if t == "Mapping[str, Any]":
        return {"k": "v"}
    return "any-value"


@pytest.mark.parametrize("path", list(MANIFEST.keys()), ids=lambda p: p.replace("/vcpcloud/api/", ""))
def test_endpoint_request_shape_and_signature(path):
    entry = MANIFEST[path]
    captured = {}

    def handler(request):
        captured["req"] = request
        return httpx.Response(200, json={"code": 200, "msg": "success", "ts": 1, "data": {}})

    client = VMOSClient(AK, SK, http_client=httpx.Client(transport=httpx.MockTransport(handler)))

    namespace = getattr(client, entry["module"])
    method = getattr(namespace, entry["method"])

    kwargs = {p["py"]: sample_for(p) for p in entry["params"]}
    result = method(**kwargs)
    assert result == {}, "data field should be returned"

    req = captured["req"]
    # 1) path + method
    assert req.url.path == path
    assert req.method == entry["http_method"]

    # 2) auth headers present
    assert req.headers["X-Access-Key"] == AK
    ts = req.headers["X-Timestamp"]
    assert ts.isdigit() and len(ts) == 10

    # 3) parameters serialized under exact API names + signature over exact bytes
    is_multipart = req.headers.get("Content-Type", "").startswith("multipart/")
    if is_multipart:
        sign_payload = ""
    elif entry["http_method"] == "GET":
        sign_payload = req.url.query.decode()
        for p in entry["params"]:
            assert f"{p['api']}=" in sign_payload, f"query param {p['api']} missing"
    else:
        sign_payload = req.content.decode("utf-8")
        sent = json.loads(sign_payload)
        for p in entry["params"]:
            if p.get("is_file"):
                continue
            assert p["api"] in sent, f"body param {p['api']} missing"

    assert req.headers["X-Sign"] == V2Signer.signature(SK, ts, path, sign_payload)


def test_manifest_covers_all_documented_endpoints():
    assert len(MANIFEST) == 152, "manifest must contain every documented endpoint"
    modules = {e["module"] for e in MANIFEST.values()}
    assert modules == {
        "instance", "apps", "tasks", "phone", "storage", "static_proxy",
        "dynamic_proxy", "email", "automation", "token", "touch",
    }


def test_no_duplicate_method_names_within_module():
    seen = set()
    for path, e in MANIFEST.items():
        key = (e["module"], e["method"])
        assert key not in seen, f"duplicate method {key} for {path}"
        seen.add(key)
