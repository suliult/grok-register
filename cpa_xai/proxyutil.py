"""Proxy helpers for CPA/OIDC export."""

import os
import threading
import urllib.parse


_tls = threading.local()


def set_runtime_proxy(proxy):
    value = str(proxy or "").strip()
    _tls.proxy = value or None


def get_runtime_proxy():
    return getattr(_tls, "proxy", None)


def resolve_proxy(explicit=None):
    for candidate in (
        str(explicit or "").strip(),
        str(get_runtime_proxy() or "").strip(),
        str(os.environ.get("https_proxy") or "").strip(),
        str(os.environ.get("HTTPS_PROXY") or "").strip(),
        str(os.environ.get("http_proxy") or "").strip(),
        str(os.environ.get("HTTP_PROXY") or "").strip(),
    ):
        if candidate:
            return candidate
    return ""


def proxy_for_chromium(proxy):
    raw = str(proxy or "").strip()
    if not raw:
        return ""
    if "://" not in raw:
        raw = "http://" + raw
    try:
        parsed = urllib.parse.urlsplit(raw)
    except Exception:
        return ""
    host = parsed.hostname or ""
    if not host:
        return ""
    port = parsed.port or (443 if (parsed.scheme or "http").lower() == "https" else 80)
    scheme = parsed.scheme or "http"
    return "%s://%s:%s" % (scheme, host, port)


def proxy_log_label(proxy):
    raw = str(proxy or "").strip()
    if not raw:
        return ""
    if "://" not in raw:
        raw = "http://" + raw
    try:
        parsed = urllib.parse.urlsplit(raw)
    except Exception:
        return "(proxy)"
    host = parsed.hostname or "?"
    port = parsed.port
    auth = "user:***@" if parsed.username else ""
    suffix = ":%s" % port if port else ""
    return "%s://%s%s%s" % (parsed.scheme or "http", auth, host, suffix)
