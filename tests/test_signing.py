"""V2 signature tests, including the official documentation test vector."""

import hashlib

from vmos.auth import V2Signer

# Official test vector from
# https://cloud.vmoscloud.com/vmoscloud/doc/en/server/example-v2.html
SK = "9cucpjoyn4xxmkhj3q9el3ce"
TS = "1747555200"
PATH = "/vcpcloud/api/padApi/padInfo"
BODY = '{"padCode":"AC32010601132"}'


def test_official_vector_signstring_concatenation():
    expected = hashlib.sha256(f"{SK}{TS}{PATH}{BODY}".encode("utf-8")).hexdigest()
    assert V2Signer.signature(SK, TS, PATH, BODY) == expected
    # 64-char lowercase hex
    sig = V2Signer.signature(SK, TS, PATH, BODY)
    assert len(sig) == 64
    assert sig == sig.lower()
    assert all(c in "0123456789abcdef" for c in sig)


def test_signature_changes_with_each_component():
    base = V2Signer.signature(SK, TS, PATH, BODY)
    assert V2Signer.signature("other", TS, PATH, BODY) != base
    assert V2Signer.signature(SK, "1747555201", PATH, BODY) != base
    assert V2Signer.signature(SK, TS, "/vcpcloud/api/padApi/restart", BODY) != base
    assert V2Signer.signature(SK, TS, PATH, "") != base


def test_headers_contain_all_three_auth_fields():
    signer = V2Signer("my_ak", SK)
    headers = signer.headers(PATH, BODY, timestamp=TS)
    assert headers["X-Access-Key"] == "my_ak"
    assert headers["X-Timestamp"] == TS
    assert headers["X-Sign"] == V2Signer.signature(SK, TS, PATH, BODY)


def test_headers_default_timestamp_is_unix_seconds():
    signer = V2Signer("ak", "sk")
    headers = signer.headers(PATH, "")
    ts = headers["X-Timestamp"]
    assert ts.isdigit()
    assert len(ts) == 10  # unix seconds, not milliseconds


def test_empty_credentials_rejected():
    import pytest

    with pytest.raises(ValueError):
        V2Signer("", "sk")
    with pytest.raises(ValueError):
        V2Signer("ak", "")
