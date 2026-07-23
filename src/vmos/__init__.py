"""VMOS Cloud Python SDK.

Unofficial, complete Python SDK for the VMOS Cloud Server OpenAPI
(cloud Android phone instances): https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html

Quickstart::

    from vmos import VMOSClient

    client = VMOSClient(access_key="ak_...", secret_key="sk_...")
    pads = client.instance.pad_detail(rows=10)

Namespaces available on the client:

======================  =====================================================
``client.instance``     Instance management (restart, properties, ADB, ...)
``client.apps``         Application management (install, start, stop, ...)
``client.tasks``        Async task status & details
``client.phone``        Cloud phone commerce (orders, renewals, backups, ...)
``client.storage``      Cloud Space (storage goods, files, backups)
``client.static_proxy`` Static residential IP service
``client.dynamic_proxy``Dynamic proxy service
``client.email``        Email verification service
``client.automation``   Flow Automation / RPA
``client.token``        SDK temporary (STS) tokens
``client.touch``        Humanized touch simulation
======================  =====================================================
"""

from ._version import __version__
from .auth import V2Signer
from .callbacks import CallbackEvent, parse_callback
from .client import DEFAULT_BASE_URL, AsyncVMOSClient, VMOSClient
from .exceptions import (
    VMOSAPIError,
    VMOSAuthError,
    VMOSError,
    VMOSHTTPError,
    VMOSRateLimitError,
)
from .models import APIResponse
from .profile import Profile, generate_profile, validate as validate_profile
from .spoof import DeviceProfile, apply_profile, verify_profile

__all__ = [
    "__version__",
    "VMOSClient",
    "AsyncVMOSClient",
    "DEFAULT_BASE_URL",
    "V2Signer",
    "APIResponse",
    "CallbackEvent",
    "parse_callback",
    "VMOSError",
    "VMOSHTTPError",
    "VMOSAPIError",
    "VMOSAuthError",
    "VMOSRateLimitError",
    "DeviceProfile",
    "apply_profile",
    "verify_profile",
    "Profile",
    "generate_profile",
    "validate_profile",
]
