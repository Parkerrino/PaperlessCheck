"""Attach CSRF only to the fixed isolated scan target."""

import os


def zap_started(zap, target):
    result = zap.replacer.add_rule(
        description="PaperlessCheck disposable CSRF",
        enabled="true",
        matchtype="REQ_HEADER",
        matchregex="false",
        matchstring="X-CSRF-Token",
        replacement=os.environ["PAPERLESS_SCAN_CSRF"],
        url=r"^http://backend:5000/.*",
    )
    if result != "OK":
        raise RuntimeError("Could not configure authenticated scan")
