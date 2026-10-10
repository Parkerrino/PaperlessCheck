# Changelog

All notable changes to PaperlessCheck are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Version numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog records implemented changes. Planned features are tracked in
the [project roadmap](README.md#roadmap).

## [Unreleased]

### Security

- Generate disposable scan database credentials per run instead of storing a fixed password.
- Document narrowly scoped scanner-job and negative-test exceptions; API authentication findings remain open.

- Reject null characters in checklist titles/descriptions and item titles before database access.
- Remove unrestricted backend CORS access; browser clients use the same-origin API proxy.
- Add `X-Content-Type-Options: nosniff` and JSON HTTP errors, preserving status and `Allow` headers.
- Add regression tests for findings from the first local ZAP pilot.


### Added

- Eight UI regression tests for the German checklist interface, deletion flows,
  duplicate submissions, preserved inputs, search reset, and progress updates.
- Configurable frontend API root with a same-origin `/api` default and Vite proxy.
- Isolated ZAP API-scan prototype with a disposable database, local reports,
  and a manual CI workflow that preserves scan artifacts. First local pilot completed with findings; remediation rescan pending.

### Changed

- German interface labels, document language, confirmations and user feedback.
- Disable conflicting actions during requests and preserve inputs after failures.
- Show checklist names in deletion confirmations and update the view after writes.
- Document frontend build-time configuration and UI acceptance evidence.
- Replace the disabled EthicalCheck placeholder with the local scan prototype.

## [1.2.1] - 2026-10-08

### Added

- Dockerfile healthchecks for the backend and frontend application images.
- Frontend Nginx health endpoint.

### Changed

- Frontend runtime uses an unprivileged Nginx image on container port 8080;
  the default browser URL remains http://localhost:3000.
- Docker Compose uses the backend image healthcheck.
- Updated README with environment setup, credential rotation, health endpoints,
  development and test commands, deployment limitations, and the 2026 roadmap.

### Security

- Run the backend and frontend application containers as non-root users.
- Replace hardcoded Compose database credentials with environment interpolation
  and require a non-empty `POSTGRES_PASSWORD`.
- Set read-only default permissions in the Docker publishing workflow while
  retaining package write permission in the publishing job.

## [1.2.0]

### Added

- Checklist search by title and description.
- Case-insensitive search with leading and trailing whitespace ignored.
- A "No checklists found" message when no entries match the search.
- Seven automated search tests covering title matches, description matches,
  case handling, surrounding whitespace, empty queries, missing matches,
  and missing or null descriptions.
- Vitest as the frontend test runner, available through `npm test`.
- Frontend test execution in CI before the production build.
- Six API validation tests covering missing, empty, whitespace-only, and
  numeric titles, JSON arrays, and malformed JSON.
- Fifteen API validation tests for invalid description types and item
  positions, verifying rejection before database access.
- Seven validator tests confirming that valid descriptions and item
  positions remain accepted.

### Changed

- Extracted checklist filtering from `App.jsx` into
  `frontend/src/utils/filterChecklists.js`.
- Pinned Ruff to version `0.16.10`.
- Removed the additional Ruff upgrade from CI to use the version declared
  in backend requirements.
- Explicitly configured first-party imports in `ruff.toml` for consistent
  import classification.

### Fixed

- Reject whitespace-only checklist and item titles.
- Reject non-object JSON payloads in checklist and item validators before
  accessing object fields.
- Reject explicitly supplied non-string descriptions, including numbers,
  booleans, arrays, objects, and null.
- Reject negative item positions.
- Reject boolean item positions instead of treating them as integers.
- Preserve support for omitted or empty string descriptions and omitted
  or non-negative integer item positions.
- Renamed the Vite configuration to `vite.config.mjs` to explicitly use
  the ES module format.

## [1.1.1] - 2026-10-06

### Added

- PostgreSQL integration test covering checklist creation, item creation,
  completion persistence, checklist deletion, and cascading item deletion.
- Frontend dependency lockfile for reproducible dependency installations.
- Docker ignore rules excluding local `node_modules` and `dist` directories
  from the frontend build context.

### Changed

- Frontend CI and Docker builds now install dependencies with `npm ci`.
- CI lint checks report violations without modifying source files.
- Updated `python-dotenv` to `1.2.4`.
- Updated GitHub Actions dependencies.

### Fixed

- Backend lint violations and import formatting.
- Flask application and test client fixtures are now provided separately
  for compatibility with pytest-flask.
- Integration tests use the client fixture without overwriting it.

### Security

- Documented support for the latest stable PaperlessCheck 1.x release.
- Added instructions for private vulnerability reporting and coordinated
  disclosure.

## [1.1.0] - 2026-10-04

### Changed

- Updated Ruff to `0.15.21`.
- Updated pytest to `9.1.1`.
- Updated Flask-CORS to `6.0.5`.
- Updated `python-dotenv` to `1.2.3`.
- Updated `psycopg2-binary` to `2.9.13`.
- Updated Black to `26.5.1`.
- Updated the frontend Docker build image from `node:22-alpine` to
  `node:26-alpine`.
- Updated GitHub Actions dependencies.

## [1.0.0] - 2026-05-04

Initial MVP release. Published on GitHub using the tag `Release`.

### Added

- Flask REST API for creating, reading, updating, and deleting checklists
  and checklist items.
- React frontend for creating, viewing, and deleting checklists, adding
  and deleting items, and toggling item completion.
- Checklist progress indicators.
- Responsive user interface with loading states and error messages.
- Input validation for checklist and item requests.
- Health check endpoints.
- PostgreSQL persistence for checklists and items.
- Database schema initialization and sample checklists.
- Cascading deletion of items when their checklist is deleted.
- Index on the checklist reference used by checklist items.
- Dockerfiles for the backend and frontend.
- Docker Compose setup for the application and database.
- Nginx configuration for serving the frontend.
- CI checks for backend linting, formatting, and tests, plus frontend builds.
- Docker image build and publishing workflow.
- Dependabot configuration.
- README, API reference, deployment instructions, and contribution guide.

### Changed

- Updated React and React DOM to `19.2.5`.
- Updated Vite to `8.0.10` and its React plugin to `6.0.1`.
- Updated Flask to `3.1.3` and Flask-CORS to `6.0.2`.
- Updated `python-dotenv` to `1.2.2`.
- Updated `psycopg2-binary` to `2.9.12`.
- Updated pytest to `9.0.3`, Black to `26.3.1`, and Ruff to `0.15.12`.

### Fixed

- Initial CI integration and lint/format checks.
- SQL schema and sample data setup for displaying the example checklists.
[Unreleased]: https://github.com/Parkerrino/PaperlessCheck/compare/v1.2.1...HEAD
[1.2.1]: https://github.com/Parkerrino/PaperlessCheck/compare/1.2.0...v1.2.1
[1.2.0]: https://github.com/Parkerrino/PaperlessCheck/compare/1.1.1...1.2.0
[1.1.1]: https://github.com/Parkerrino/PaperlessCheck/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/Parkerrino/PaperlessCheck/compare/Release...1.1.0
[1.0.0]: https://github.com/Parkerrino/PaperlessCheck/releases/tag/Release
