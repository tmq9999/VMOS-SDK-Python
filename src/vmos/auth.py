"""VMOS Cloud OpenAPI authentication.

Implements the **V2 Simplified Signature** scheme (recommended by VMOS for all
new integrations):

    signString = SK + X-Timestamp + path + bodyOrQuery
    X-Sign     = lowerHex( SHA-256( signString_UTF8 ) )

Headers sent with every request:

    X-Access-Key : Access Key ID (plain text)
    X-Timestamp  : unix seconds (10-digit string, ±5-minute window)
    X-Sign       : 64-char lowercase hex signature

``bodyOrQuery`` rules (per official docs):

* ``POST``/``PUT`` JSON  -> the raw body **exactly as sent** (no re-ordering,
  no whitespace stripping).
* ``GET``                -> the raw query string exactly as sent
  (e.g. ``a=1&b=2``); empty string when there are no parameters.
* File uploads (multipart) -> empty string (the file body is not signed).

Reference: https://cloud.vmoscloud.com/vmoscloud/doc/en/server/example-v2.html
"""

from __future__ import annotations

import hashlib
import time
from typing import Dict, Optional

__all__ = ["V2Signer"]


class V2Signer:
    """Computes VMOS V2 simplified signatures.

    Example
    -------
    >>> signer = V2Signer("my_ak", "my_sk")
    >>> headers = signer.headers("/vcpcloud/api/padApi/padInfo",
    ...                          '{"padCode":"AC32010601132"}')
    >>> sorted(headers)
    ['X-Access-Key', 'X-Sign', 'X-Timestamp']
    """

    def __init__(self, access_key: str, secret_key: str) -> None:
        if not access_key or not secret_key:
            raise ValueError(
                "access_key and secret_key are required. Get them from the "
                "VMOS console: Developer -> API."
            )
        self.access_key = access_key
        self._secret_key = secret_key

    @staticmethod
    def signature(secret_key: str, timestamp: str, path: str, body_or_query: str) -> str:
        """Return ``lowerHex(SHA-256(SK + timestamp + path + bodyOrQuery))``.

        Plain string concatenation with **no delimiters**, exactly as specified
        by the official V2 documentation.
        """
        sign_string = f"{secret_key}{timestamp}{path}{body_or_query}"
        return hashlib.sha256(sign_string.encode("utf-8")).hexdigest()

    def headers(
        self,
        path: str,
        body_or_query: str,
        timestamp: Optional[str] = None,
    ) -> Dict[str, str]:
        """Build the three V2 authentication headers for a request.

        Parameters
        ----------
        path:
            Full request path including the servlet prefix,
            e.g. ``/vcpcloud/api/padApi/padInfo``.
        body_or_query:
            Exact payload string participating in the signature (see module
            docstring for the rules).
        timestamp:
            Optional unix-seconds string; defaults to the current time.
        """
        ts = timestamp if timestamp is not None else str(int(time.time()))
        return {
            "X-Access-Key": self.access_key,
            "X-Timestamp": ts,
            "X-Sign": self.signature(self._secret_key, ts, path, body_or_query),
        }
