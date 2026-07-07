# PaperlessCheck - Task Tracking

## CICD Pipeline (GitHub Actions)

- [x] Create CI workflow (`.github/workflows/ci.yml`) for backend (ruff/black/pytest + Postgres service) and frontend (npm build)
- [x] Create Docker build/push workflow (`.github/workflows/docker-build-push.yml`) to push images to GHCR on version tags
- [ ] Optional: add dependabot configuration
- [ ] Optional: add workflow to build/push images on pushes to main/develop (in addition to tags)
- [ ] Run a local verification (optional): `act` or trigger workflows in GitHub

