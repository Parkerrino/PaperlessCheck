# PaperlessCheck

PaperlessCheck is a self-hosted checklist application built with Flask, React,
and PostgreSQL. Create checklists, track item completion, and find checklists
by title or description.

## Features

- Create and delete checklists and checklist items.
- Mark items as completed and view checklist progress.
- Use the German interface, named deletion confirmations, visible save states,
  preserved inputs after errors, and search reset.
- Search checklist titles and descriptions, ignoring case and surrounding whitespace.
- Store checklists and items in PostgreSQL.
- Validate API input before accessing the database for rejected requests.
- Run the application with Docker Compose.
- Run backend and frontend application containers as non-root users.
- Check application container health through Docker healthchecks.

The REST API also provides update endpoints for checklists and items.

## Requirements

For the complete application:

- Docker with the Compose plugin (`docker compose`).
- A running Docker engine using Linux containers.
- Available host ports 3000 and 5000.

For development and tests outside containers:

- Python 3.12, matching backend CI.
- Node.js 22, matching frontend CI; use an up-to-date patch release compatible
  with the packages in `frontend/package-lock.json`.
- PostgreSQL 16 for backend integration tests.

The frontend Docker build currently uses Node.js 26. Exact Python dependencies
are declared in `backend/requirements.txt`; frontend dependency versions are
resolved in `frontend/package-lock.json`.

## Quick start

### 1. Clone the repository

```sh
git clone https://github.com/Parkerrino/PaperlessCheck.git
cd PaperlessCheck
```

### 2. Configure the database credentials

Create `.env` in the repository root from `.env.example`.
For an existing installation, edit the existing `.env` instead of overwriting it.

PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux or macOS:

```sh
cp .env.example .env
```

Set these values in `.env`:

```dotenv
POSTGRES_USER=paperless
POSTGRES_PASSWORD=
POSTGRES_DB=paperlesscheck
```

Fill in `POSTGRES_PASSWORD` with a long, unique password before starting.
The empty value above is intentional: Compose refuses to start without a password.
Use a randomly generated alphanumeric password for this configuration because
Compose inserts it directly into the database connection URL. Characters with
special meaning in URLs require appropriate encoding in a connection URL.

Keep `.env` out of version control. `.env.example` is the shareable template.

Compose constructs `DATABASE_URL` for the backend using the database service
hostname `db`. It explicitly sets `FLASK_ENV=production`; the development setting
in `.env.example` does not override that Compose value.

### 3. Build and start

Run from the repository root:

```sh
docker compose up -d --build
docker compose ps
```

Wait for the backend and frontend to report healthy.

| Service | Address | Purpose |
| --- | --- | --- |
| Frontend | http://localhost:3000 | Checklist interface |
| Backend | http://localhost:5000 | Flask API |
| PostgreSQL | `db:5432` inside Compose | Persistent database |

The frontend maps host port 3000 to container port 8080.
PostgreSQL is not published on a host port by the default Compose configuration.

### 4. Verify the application

Create a temporary checklist, add an item, mark it complete, and reload the page
to check persistence. Search for the checklist by title and description, then
delete the temporary checklist.

## Healthchecks and logs

| Endpoint | What it checks |
| --- | --- |
| `http://localhost:3000/health` | Frontend Nginx responds |
| `http://localhost:5000/health` | Backend application responds |
| `http://localhost:5000/api/checklists/health` | Backend can connect to PostgreSQL |

The application container healthchecks use their respective `/health` endpoints.
A healthy backend container does not by itself confirm database connectivity.
The frontend waits for the backend container to become healthy before starting.

```sh
docker compose ps
docker compose logs --tail=100 backend frontend db
docker compose logs -f backend
```

In PowerShell, check the endpoints with:

```powershell
Invoke-RestMethod http://localhost:3000/health
Invoke-RestMethod http://localhost:5000/health
Invoke-RestMethod http://localhost:5000/api/checklists/health
```

## Database persistence and credentials

PostgreSQL stores data in the named Compose volume `paperlesscheck_db_data`.
Compose normally prefixes the actual Docker volume name with the project name.
The initialization script is `database/init.sql`, mounted into the PostgreSQL
initialization directory. Initialization runs when the database data directory
is first created; changing this script does not migrate an existing database.

Stop the application while preserving its database volume:

```sh
docker compose down
```

Do not add `-v` unless you intend to delete the database volume and its contents.
Back up existing data before upgrades or database changes.

Changing `POSTGRES_PASSWORD` in `.env` does not change the password of a role in
an existing database volume. To rotate the password for the default user:

```sh
docker compose exec db psql -U paperless -d paperlesscheck
```

At the PostgreSQL prompt:

```text
\password paperless
\q
```

Enter the new password when prompted, update `.env` to match, then run
`docker compose up -d` to apply the changed container environment. Substitute
your configured user and database if you changed the defaults.

## Development

### Frontend with the Docker backend

Start the database and backend from the repository root:

```sh
docker compose up -d --build backend
```

Then start Vite:

```sh
cd frontend
npm ci
npm run start
```

Open the URL printed by Vite, normally http://localhost:5173.
The frontend requests `/api/checklists` on its own origin by default. Vite forwards
`/api` to `http://127.0.0.1:5000` during development and preview. Docker Nginx
already forwards `/api/` to the backend service.

To customize, copy `frontend/.env.example` to `frontend/.env.local`:

```dotenv
VITE_API_BASE_URL=/api
API_PROXY_TARGET=http://127.0.0.1:5000
```

`VITE_API_BASE_URL` is the API root **without** `/checklists`; it can be a
root-relative path such as `/api` or a full HTTP(S) URL ending in `/api`.
Keep `/api` for same-origin deployment and normal Vite development. If using a
custom relative prefix, configure the reverse proxy for that prefix too.
The backend does not grant cross-origin browser access by default. Use the
same-origin `/api` proxy. An absolute cross-origin URL additionally requires an
explicit, restricted CORS/HTTPS configuration at your deployment proxy.
No credentials or secrets belong in `VITE_*`: they are public browser code.
`API_PROXY_TARGET` is used only by the Vite server, not by the browser.

Vite substitutes the API root at build time. Restart Vite after configuration
changes; rebuild production assets. For Compose, set `VITE_API_BASE_URL=/api`
in the repository-root `.env` and run `docker compose up -d --build frontend`.
The frontend Dockerfile exposes the same build argument for direct Docker builds.
Changing an environment variable on an already-built Nginx container does not
change the API address. Published images use their build-time configuration.

Before deployment, verify from a second computer that requests go to
`http(s)://<frontend-host>/api/checklists`, not that computer's localhost.
IIS must forward `/api` to the backend for the same-origin default. This change
does not implement IIS authentication, MSSQL support, or deployment approval.

### Backend outside Docker

Use a reachable PostgreSQL 16 database with the schema from `database/init.sql`
already initialized. The default Compose database has no host port, so it cannot
be reached at `localhost:5432` without an explicit local port mapping.
Stop any container using port 5000 before running a local backend on that port.

From the repository root, using PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
$env:DATABASE_URL = 'postgresql://YOUR_USER:YOUR_URL_ENCODED_PASSWORD@localhost:5432/YOUR_DATABASE'
$env:FLASK_ENV = 'development'
python backend/app.py
```

Replace all connection placeholders with your local development settings.
On Linux or macOS, activate the environment with `source .venv/bin/activate`
and set environment variables with `export`.

## Automated checks

### Frontend

From the repository root:

```sh
cd frontend
npm ci
npm test
npm run build
```

`npm test` runs Vitest once. Search tests cover title and description matches,
case-insensitive matching, surrounding whitespace, empty queries, no matches,
and missing or null descriptions.

### Backend

With the virtual environment activated, from the repository root:

```sh
python -m pip install -r backend/requirements.txt
cd backend
python -m ruff check .
python -m black --check .
```

Run the validation test files without requiring a live application database:

```sh
python -m pytest -q tests/test_checklist_validation.py tests/test_validation_edge_cases.py
```

For the full test suite, first configure `DATABASE_URL` to point to a dedicated
test database initialized from `database/init.sql`. Do not use a database holding
important application data: integration tests create and delete records.

PowerShell, from `backend`:

```powershell
$env:DATABASE_URL = 'postgresql://YOUR_TEST_USER:YOUR_URL_ENCODED_PASSWORD@localhost:5432/YOUR_TEST_DATABASE'
$env:FLASK_ENV = 'test'
python -m pytest -q
```

The CI workflow provisions PostgreSQL 16, initializes the schema, and runs the
backend checks with Python 3.12. The frontend job uses Node.js 22 and runs
`npm ci`, `npm test`, and `npm run build`.

## Local API security scan

A ZAP API-scan prototype replaces the disabled EthicalCheck placeholder. It uses
a separate Docker Compose stack with disposable PostgreSQL data and an internal
network. It does not contact a production or internal deployment.

```sh
python scripts/security_scan.py
```

Reports and diagnostics are saved under `reports/paperless-scan-<id>/`.
See [the scan guide](docs/api-security-scan.md) for prerequisites, findings policy,
manual CI execution, limitations, and the first pilot findings and pending remediation rescan.

## API reference

The checklist API base path is `/api/checklists`.

| Method | Path | Operation |
| --- | --- | --- |
| GET | `/api/checklists` | List checklists |
| POST | `/api/checklists` | Create a checklist |
| GET | `/api/checklists/<checklist_id>` | Get a checklist |
| PUT | `/api/checklists/<checklist_id>` | Update a checklist |
| DELETE | `/api/checklists/<checklist_id>` | Delete a checklist and its items |
| POST | `/api/checklists/<checklist_id>/items` | Add an item |
| PUT | `/api/checklists/items/<item_id>` | Update an item |
| DELETE | `/api/checklists/items/<item_id>` | Delete an item |

Send request bodies as JSON with `Content-Type: application/json`.
Example checklist creation body:

```json
{
  "title": "Project setup",
  "description": "Tasks for the next release"
}
```

Titles must be non-empty strings containing more than whitespace.
Descriptions may be omitted or provided as strings, including empty strings.
Explicit `null` descriptions are rejected by validation.
Item positions (`order_index`) may be omitted or supplied as non-negative
integers; booleans are rejected.

## Troubleshooting

- **Docker engine unavailable:** Start Docker Desktop or the Docker daemon and
  check that Linux containers are enabled.
- **Missing password:** Set `POSTGRES_PASSWORD` in the root `.env` file.
- **Database authentication fails after editing `.env`:** Update the existing
  PostgreSQL role password too; see the credential rotation instructions above.
- **Backend cannot reach the database:** Check `docker compose logs db backend`
  and the database-aware health endpoint. On first startup, PostgreSQL may still
  be initializing; backend process health alone does not establish readiness.
- **Frontend cannot reach the API:** Confirm that the backend is reachable on
  its configured proxy target. Inspect `/api/checklists` in the browser network
  tab and check Nginx/Vite proxy logs; rebuild after changing the API root.
- **Port already in use:** Stop the conflicting service or adjust Compose port
  mappings. For local Vite development, update `API_PROXY_TARGET` if the backend
  host port changes. Docker Nginx uses the internal backend port.

## Security and deployment scope

The current application has no built-in user authentication or authorization.
Use it in a trusted environment with appropriate network access controls.
The default Compose configuration publishes the frontend and backend on the
host's network interfaces; it is not restricted to loopback.

Both application containers run as non-root users. This reduces container
privileges but does not provide user authentication or make the application
suitable for unrestricted public access.

The backend currently starts with `python app.py`. Setting `FLASK_ENV=production`
does not replace Flask's development server with a production WSGI server.
Production server setup and deployment improvements remain planned work.

See [SECURITY.md](SECURITY.md) for supported versions and private vulnerability
reporting instructions.

## Roadmap

These are planning targets for the remainder of 2026, not promised release dates.
Existing loading states, error messages, and progress indicators will be improved
rather than introduced as entirely new features.

| Target | Focus |
| --- | --- |
| 1.2.1, October | Container hardening and documentation |
| 1.3.0, October | Better loading, empty and error states; deletion confirmation; sorting |
| 1.4.0, early November | Validated JSON import/export and documented backup/restore |
| 1.5.0, late November | Checklist duplication with reset completion state; status filters; progress refinements |
| 1.6.0, early December | Production backend server, readiness checks, logs and update instructions |
| Late December | Stabilization, maintenance and installation/update verification |

Authentication, roles, and collaboration require separate design work and are
planned for consideration in 2027. Longer-term ideas include categories, due
dates, recurring checklists, templates, PDF/Excel export, dark mode, and webhooks.

## Contributing

Create a branch or fork, make a focused change, and add tests where applicable.
Run the relevant checks before opening a pull request. Include documentation
updates for changed setup steps or behavior.

Report bugs and feature requests through
[GitHub Issues](https://github.com/Parkerrino/PaperlessCheck/issues).
See [CHANGELOG.md](CHANGELOG.md) for recorded changes.

## License

PaperlessCheck is available under the MIT License. See [LICENSE](LICENSE).
