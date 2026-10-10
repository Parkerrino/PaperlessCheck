# Local API security scan — prototype

## Status

Prepared for local Docker execution and a manually triggered GitHub Actions pilot.
The full ZAP/PostgreSQL run has NOT been executed in the preparation environment:
Docker is unavailable there. Static configuration checks and frontend tests are
separate evidence, not proof of a completed security scan.

## Scope

ZAP actively scans the API operations in `security/openapi.json`, including write
and delete operations. `compose.security.yml` is a standalone stack: no published
ports, an internal runtime network, no application data volume, and PostgreSQL
on tmpfs. Initialization uses repository sample data. The runner chooses a unique
Compose project and removes only that stack afterward. Builds/image pulls need
internet access; scan containers do not have external network access.

The target is fixed to `http://backend:5000`. Do not replace it with a live or
internal deployment. The runner has no user-supplied target argument. Temporary
scan credentials are test fixtures and are not production credentials.

## Local run (PowerShell, Linux or macOS)

From the repository root, with Python 3 and Docker Compose installed and running:

```sh
python scripts/security_scan.py
```

No production `.env` is required. Do not combine this Compose file with the
application Compose file. The runner builds the images, waits for database-aware
backend health, scans, copies reports, writes diagnostics, and tears down the
stack. On cancellation, cleanup is attempted; if the process is forcibly killed,
use the project name printed in `reports/` to remove that specific scan stack.

```sh
docker compose -f compose.security.yml -p <scan-project-name> down --volumes --remove-orphans
docker rm -f <scan-project-name>-zap
```

## Reports and exit policy

Each run has its own `reports/paperless-scan-<id>/` directory:

- `report.html`, `report.json`, `report.md`: ZAP findings.
- `summary.json`: run status, target, counts and exit code.
- `services.log`, `scanner.log`, `images.json`: diagnostics and image identities.

Runner exit 0 means the scan completed with no high-risk findings; lower-risk
warnings can still exist and must be reviewed. Exit 1 means high-risk findings or
ZAP FAIL rules. Exit 3 means an infrastructure/report/cleanup failure. Missing
reports or an empty site list never count as a successful scan. All warning
findings remain in the reports; none are silently ignored.

The prototype uses the mutable ZAP `stable` image and PostgreSQL 16 tag; image
identities are recorded. After the first successful pilot, choose reviewed image
digests for repeatable runs and define the repository's findings policy.

## CI pilot

The existing `.github/workflows/ethicalcheck.yml` becomes **Local API security
scan (ZAP prototype)**. It has only a manual `workflow_dispatch` trigger initially,
read-only repository permissions, a disposable hosted runner and no secrets.
The artifact upload runs even on scan failure, preserving reports for 14 days.
After merging the reviewed workflow, run it through Actions and inspect the
artifact. Enable pull-request triggers only after validating this pilot.
Do not use `pull_request_target` to run untrusted branch code with elevated access.

## Limits and next acceptance steps

- [ ] Run the full prototype locally with Docker and inspect HTML/JSON reports.
- [ ] Verify actual route coverage and review findings, including expected header warnings.
- [ ] Confirm diagnostics survive a failed scan and teardown removes the test stack.
- [ ] Run the manual CI pilot and download its artifact.
- [ ] Pin reviewed images and decide which additional findings should fail CI.

The OpenAPI file is a scan contract, not a verified complete public API specification.
Destructive endpoints may invalidate sample IDs during the scan; inspect coverage
before claiming all CRUD paths were exercised successfully. The current scan does
not prove authentication, authorization, CSRF protection or business-logic safety.
It complements unit/integration tests and is not a full EthicalCheck-equivalent
security assurance. Application auth and the internal fork remain separate work.

Reference: https://www.zaproxy.org/docs/docker/api-scan/
