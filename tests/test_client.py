"""Client behavior tests: signing on the wire, error mapping, GET/POST/multipart."""

import json

import httpx
import pytest

from vmos import (
    APIResponse,
    AsyncVMOSClient,
    VMOSAPIError,
    VMOSAuthError,
    VMOSClient,
    VMOSHTTPError,
    VMOSRateLimitError,
)
from vmos.auth import V2Signer

AK, SK = "test_ak", "test_sk"


def make_client(handler):
    transport = httpx.MockTransport(handler)
    return VMOSClient(AK, SK, http_client=httpx.Client(transport=transport))


def ok_response(data=None):
    return httpx.Response(200, json={"code": 200, "msg": "success", "ts": 1, "data": data})


def test_post_signs_exact_body_sent():
    captured = {}

    def handler(request):
        captured["request"] = request
        return ok_response({"x": 1})

    client = make_client(handler)
    data = client.request("POST", "/vcpcloud/api/padApi/padInfo", json_body={"padCode": "AC1"})
    assert data == {"x": 1}

    req = captured["request"]
    body = req.content.decode("utf-8")
    assert body == '{"padCode":"AC1"}'  # compact, exactly as signed
    assert req.headers["Content-Type"] == "application/json"
    expected = V2Signer.signature(SK, req.headers["X-Timestamp"], "/vcpcloud/api/padApi/padInfo", body)
    assert req.headers["X-Sign"] == expected
    assert req.headers["X-Access-Key"] == AK


def test_get_signs_exact_query_string():
    captured = {}

    def handler(request):
        captured["request"] = request
        return ok_response([])

    client = make_client(handler)
    client.request("GET", "/vcpcloud/api/padApi/getEmailOrder", query={"page": 1, "size": 10})

    req = captured["request"]
    qs = req.url.query.decode()
    assert qs == "page=1&size=10"
    expected = V2Signer.signature(SK, req.headers["X-Timestamp"], "/vcpcloud/api/padApi/getEmailOrder", qs)
    assert req.headers["X-Sign"] == expected


def test_get_without_params_signs_empty_string():
    captured = {}

    def handler(request):
        captured["request"] = request
        return ok_response([])

    client = make_client(handler)
    client.request("GET", "/vcpcloud/api/padApi/country", query=None)

    req = captured["request"]
    assert req.url.query == b""
    expected = V2Signer.signature(SK, req.headers["X-Timestamp"], "/vcpcloud/api/padApi/country", "")
    assert req.headers["X-Sign"] == expected


def test_multipart_upload_signs_empty_string():
    captured = {}

    def handler(request):
        captured["request"] = request
        return ok_response({"fileId": "f1"})

    client = make_client(handler)
    client.request(
        "POST",
        "/vcpcloud/api/padApi/uploadFile",
        files={"file": ("app.apk", b"\x00\x01")},
    )

    req = captured["request"]
    assert req.headers["Content-Type"].startswith("multipart/form-data")
    expected = V2Signer.signature(SK, req.headers["X-Timestamp"], "/vcpcloud/api/padApi/uploadFile", "")
    assert req.headers["X-Sign"] == expected


def test_none_values_dropped_from_json_body():
    captured = {}

    def handler(request):
        captured["request"] = request
        return ok_response()

    client = make_client(handler)
    client.instance.pad_detail(rows=5)  # all other optionals None
    sent = json.loads(captured["request"].content)
    assert sent == {"rows": 5}


def test_business_error_raises_api_error():
    client = make_client(lambda r: httpx.Response(200, json={"code": 1002, "msg": "User ID cannot be empty", "ts": 1}))
    with pytest.raises(VMOSAPIError) as ei:
        client.request("POST", "/vcpcloud/api/padApi/padInfo", json_body={})
    assert ei.value.code == 1002
    assert "User ID" in ei.value.msg


@pytest.mark.parametrize("code", [2019, 2031, 2032, 2033])
def test_auth_errors_map_to_auth_subclass(code):
    client = make_client(lambda r: httpx.Response(200, json={"code": code, "msg": "auth", "ts": 1}))
    with pytest.raises(VMOSAuthError):
        client.request("POST", "/vcpcloud/api/padApi/padInfo", json_body={})


def test_rate_limit_error_subclass():
    client = make_client(lambda r: httpx.Response(200, json={"code": 1218, "msg": "too fast", "ts": 1}))
    with pytest.raises(VMOSRateLimitError):
        client.touch.simulate_click(["P1"], 1, 2)


def test_http_error_raises_http_error():
    client = make_client(lambda r: httpx.Response(502, text="bad gateway"))
    with pytest.raises(VMOSHTTPError) as ei:
        client.request("POST", "/vcpcloud/api/padApi/padInfo", json_body={})
    assert ei.value.status_code == 502


def test_request_raw_returns_envelope_without_raising():
    client = make_client(lambda r: httpx.Response(200, json={"code": 1002, "msg": "nope", "ts": 9, "data": None}))
    env = client.request_raw("POST", "/vcpcloud/api/padApi/padInfo", json_body={})
    assert isinstance(env, APIResponse)
    assert env.code == 1002 and not env.ok and env.ts == 9


def test_env_var_credentials(monkeypatch):
    monkeypatch.setenv("VMOS_ACCESS_KEY", "env_ak")
    monkeypatch.setenv("VMOS_SECRET_KEY", "env_sk")
    captured = {}

    def handler(request):
        captured["request"] = request
        return ok_response()

    client = VMOSClient(http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    client.request("POST", "/vcpcloud/api/padApi/padInfo", json_body={})
    assert captured["request"].headers["X-Access-Key"] == "env_ak"


def test_missing_credentials_raise(monkeypatch):
    monkeypatch.delenv("VMOS_ACCESS_KEY", raising=False)
    monkeypatch.delenv("VMOS_SECRET_KEY", raising=False)
    with pytest.raises(ValueError):
        VMOSClient()


def test_unicode_body_signed_as_sent():
    captured = {}

    def handler(request):
        captured["request"] = request
        return ok_response()

    client = make_client(handler)
    client.request("POST", "/vcpcloud/api/padApi/updatePadName", json_body={"padName": "điện thoại 云机"})
    req = captured["request"]
    body = req.content.decode("utf-8")
    assert "điện thoại 云机" in body  # ensure_ascii=False - signed exactly as sent
    expected = V2Signer.signature(SK, req.headers["X-Timestamp"], "/vcpcloud/api/padApi/updatePadName", body)
    assert req.headers["X-Sign"] == expected


@pytest.mark.anyio
async def test_async_client_signs_and_parses():
    captured = {}

    def handler(request):
        captured["request"] = request
        return ok_response({"ok": True})

    transport = httpx.MockTransport(handler)
    async with AsyncVMOSClient(AK, SK, http_client=httpx.AsyncClient(transport=transport)) as client:
        data = await client.phone.pad_info("AC1")
    assert data == {"ok": True}
    req = captured["request"]
    body = req.content.decode()
    assert body == '{"padCode":"AC1"}'
    assert req.headers["X-Sign"] == V2Signer.signature(SK, req.headers["X-Timestamp"], "/vcpcloud/api/padApi/padInfo", body)


@pytest.fixture
def anyio_backend():
    return "asyncio"
