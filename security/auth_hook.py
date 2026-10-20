"""Attach and verify authentication only for the fixed isolated scan target."""

import json
import os


def zap_started(zap, target):
    for header, value in [
        ("Cookie", os.environ["ZAP_AUTH_HEADER_VALUE"]),
        ("X-CSRF-Token", os.environ["PAPERLESS_SCAN_CSRF"]),
    ]:
        result = zap.replacer.add_rule(
            description="PaperlessCheck disposable " + header,
            enabled="true",
            matchtype="REQ_HEADER",
            matchregex="false",
            matchstring=header,
            replacement=value,
            url=r"^http://backend:5000/.*",
        )
        if result != "OK":
            raise RuntimeError("Could not configure authenticated scan")

    def request(method, path, body=""):
        raw = (
            f"{method} http://backend:5000{path} HTTP/1.1\r\n"
            "Host: backend:5000\r\nContent-Type: application/json\r\n"
            f"Content-Length: {len(body.encode())}\r\n\r\n{body}"
        )
        messages = zap.core.send_request(raw, followredirects="false")
        message = messages[-1]
        return int(message["responseHeader"].split()[1]), message["responseBody"]

    status, _ = request("GET", "/api/checklists")
    if status != 200:
        raise RuntimeError("ZAP itself cannot read authenticated checklist API")
    status, body = request(
        "POST", "/api/checklists", json.dumps({"title": "ZAP auth probe"})
    )
    if status != 201:
        raise RuntimeError("ZAP itself cannot write using session and CSRF")
    checklist_id = json.loads(body)["id"]
    if request("DELETE", f"/api/checklists/{checklist_id}")[0] != 200:
        raise RuntimeError("ZAP auth probe cleanup failed")
    print("PAPERLESS_ZAP_AUTH_PREFLIGHT_OK", flush=True)
