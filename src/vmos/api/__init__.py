"""Generated VMOS API namespaces."""

from __future__ import annotations

from .apps import AppsAPI, AsyncAppsAPI
from .automation import AutomationAPI, AsyncAutomationAPI
from .dynamic_proxy import DynamicProxyAPI, AsyncDynamicProxyAPI
from .email import EmailAPI, AsyncEmailAPI
from .instance import InstanceAPI, AsyncInstanceAPI
from .phone import PhoneAPI, AsyncPhoneAPI
from .static_proxy import StaticProxyAPI, AsyncStaticProxyAPI
from .storage import StorageAPI, AsyncStorageAPI
from .tasks import TasksAPI, AsyncTasksAPI
from .token import TokenAPI, AsyncTokenAPI
from .touch import TouchAPI, AsyncTouchAPI

SYNC_NAMESPACES = {
    "apps": AppsAPI,
    "automation": AutomationAPI,
    "dynamic_proxy": DynamicProxyAPI,
    "email": EmailAPI,
    "instance": InstanceAPI,
    "phone": PhoneAPI,
    "static_proxy": StaticProxyAPI,
    "storage": StorageAPI,
    "tasks": TasksAPI,
    "token": TokenAPI,
    "touch": TouchAPI,
}

ASYNC_NAMESPACES = {
    "apps": AsyncAppsAPI,
    "automation": AsyncAutomationAPI,
    "dynamic_proxy": AsyncDynamicProxyAPI,
    "email": AsyncEmailAPI,
    "instance": AsyncInstanceAPI,
    "phone": AsyncPhoneAPI,
    "static_proxy": AsyncStaticProxyAPI,
    "storage": AsyncStorageAPI,
    "tasks": AsyncTasksAPI,
    "token": AsyncTokenAPI,
    "touch": AsyncTouchAPI,
}

__all__ = [
    "AppsAPI", "AsyncAppsAPI",
    "AutomationAPI", "AsyncAutomationAPI",
    "DynamicProxyAPI", "AsyncDynamicProxyAPI",
    "EmailAPI", "AsyncEmailAPI",
    "InstanceAPI", "AsyncInstanceAPI",
    "PhoneAPI", "AsyncPhoneAPI",
    "StaticProxyAPI", "AsyncStaticProxyAPI",
    "StorageAPI", "AsyncStorageAPI",
    "TasksAPI", "AsyncTasksAPI",
    "TokenAPI", "AsyncTokenAPI",
    "TouchAPI", "AsyncTouchAPI",
    "SYNC_NAMESPACES", "ASYNC_NAMESPACES",
]
