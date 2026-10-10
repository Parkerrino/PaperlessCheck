"""Run ZAP only against a disposable Compose stack. Requires Docker Compose."""
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    project = "paperless-scan-" + uuid.uuid4().hex[:10]
    container = project + "-zap"
    output = ROOT / "reports" / project
    output.mkdir(parents=True)
    compose = ["docker", "compose", "-f", str(ROOT / "compose.security.yml"), "-p", project]
    metadata = {"project": project, "started": datetime.now(timezone.utc).isoformat(), "target": "http://backend:5000", "status": "infrastructure-error"}
    exit_code = 3

    def run(args, **kwargs):
        return subprocess.run(args, cwd=ROOT, text=True, **kwargs)

    try:
        run(compose + ["build"], check=True, timeout=900)
        run(compose + ["up", "-d", "--wait", "--wait-timeout", "120", "backend"], check=True, timeout=180)
        result = run(compose + ["run", "--no-deps", "--name", container, "scanner"], timeout=1200)
        metadata["zap_exit_code"] = result.returncode
        reports_ok = True
        for name in ["report.html", "report.json", "report.md"]:
            copied = run(["docker", "cp", f"{container}:/zap/wrk/{name}", str(output / name)])
            reports_ok = reports_ok and copied.returncode == 0 and (output / name).exists()
        if reports_ok and result.returncode in (0, 1, 2):
            report = json.loads((output / "report.json").read_text())
            sites = report.get("site", [])
            if not sites:
                raise ValueError("ZAP report contains no scanned site")
            if any(site.get("@host") != "backend" for site in sites):
                raise ValueError("Unexpected scan target in report")
            alerts = [alert for site in sites for alert in site.get("alerts", [])]
            high = [a for a in alerts if int(a.get("riskcode", 0)) >= 3]
            metadata.update(alert_count=len(alerts), high_risk_count=len(high))
            # WARN remains visible in reports; high-risk findings fail independently.
            exit_code = 1 if high or result.returncode == 1 else 0
            metadata["status"] = "findings-failed" if exit_code else ("warnings" if alerts or result.returncode == 2 else "passed")
    except (OSError, subprocess.SubprocessError, ValueError, TypeError) as exc:
        metadata["error"] = str(exc)
    finally:
        for name, command in [("services.log", compose + ["logs", "--no-color"]), ("scanner.log", ["docker", "logs", container]), ("images.json", compose + ["images", "--format", "json"])]:
            try:
                result = run(command, capture_output=True, timeout=30)
                (output / name).write_text(result.stdout + result.stderr)
            except (OSError, subprocess.SubprocessError):
                pass
        try:
            run(["docker", "rm", "-f", container], capture_output=True, timeout=30)
            cleanup = run(compose + ["down", "--volumes", "--remove-orphans"], timeout=60)
            if cleanup.returncode:
                metadata["cleanup_failed"] = True
                exit_code = 3
        except (OSError, subprocess.SubprocessError):
            metadata["cleanup_failed"] = True
            exit_code = 3
        metadata["exit_code"] = exit_code
        (output / "summary.json").write_text(json.dumps(metadata, indent=2) + "\n")
        print(f"Reports: {output}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
