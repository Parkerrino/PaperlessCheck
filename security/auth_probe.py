"""Run via stdin inside only the disposable backend; never against a live URL."""

import http.cookiejar
import json
import os
import urllib.error
import urllib.request

from auth import store

BASE = "http://127.0.0.1:5000"


def call(opener, path, data=None, headers=None, method=None):
    request = urllib.request.Request(
        BASE + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Content-Type": "application/json", **(headers or {})},
        method=method,
    )
    try:
        with opener.open(request, timeout=15) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, {}


anonymous = urllib.request.build_opener()
assert call(anonymous, "/api/checklists")[0] == 401
if os.getenv("PAPERLESS_SCAN_VERIFY") == "1":
    auth_headers = {"Cookie": os.environ["ZAP_AUTH_HEADER_VALUE"]}
    assert call(anonymous, "/api/checklists", headers=auth_headers)[0] == 200
    print(json.dumps({"authenticated_after_scan": True, "anonymous_denied": True}))
else:
    store.init_schema()
    store.create_user("zap_scan", os.environ["PAPERLESS_SCAN_LOGIN_PASSWORD"])
    jar = http.cookiejar.CookieJar()
    browser = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    status, data = call(
        browser,
        "/api/auth/login",
        {
            "username": "zap_scan",
            "password": os.environ["PAPERLESS_SCAN_LOGIN_PASSWORD"],
        },
        {"X-Paperless-Login": "1"},
    )
    assert status == 200
    assert call(browser, "/api/checklists")[0] == 200
    assert call(browser, "/api/checklists", {"title": "CSRF must reject"})[0] == 403
    cookie = next(c.value for c in jar if c.name == "paperless_session")
    print(
        json.dumps(
            {"cookie": "paperless_session=" + cookie, "csrf": data["csrf_token"]}
        )
    )
