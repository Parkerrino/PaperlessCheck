# Changelog

All notable changes to PaperlessCheck will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-10-06

### Added
- PostgreSQL integration test covering checklist creation, item creation,
  completion persistence, and cascading deletion.
- Frontend dependency lockfile for reproducible installations.
- Docker ignore rules excluding local `node_modules` and `dist`.

### Changed
- Frontend CI and Docker builds now use `npm ci`.
- CI lint checks report violations without modifying source files.
- Security policy now documents supported releases and private
  vulnerability reporting.

### Fixed
- Backend lint violations and import formatting.
- Test fixtures now provide the Flask application and test client separately,
  ensuring compatibility with pytest-flask.
  
## [1.0.0] - 2026-05-04

### Added - MVP Release

#### Backend Features
- ✅ Flask REST API with PostgreSQL integration
- ✅ Complete CRUD operations for checklists
- ✅ Complete CRUD operations for checklist items
- ✅ Input validation service
- ✅ Health check endpoint for Docker
- ✅ CORS support for cross-origin requests
- ✅ Docker containerization
- ✅ Comprehensive error handling

#### Frontend Features
- ✅ React-based user interface with Vite
- ✅ Create and manage multiple checklists
- ✅ Add, edit, and delete checklist items
- ✅ Check/uncheck items with completion tracking
- ✅ Progress visualization (completed items count)
- ✅ Responsive design for desktop and mobile
- ✅ Real-time UI updates
- ✅ Error notifications

#### Database
- ✅ PostgreSQL database with automated schema
- ✅ Sample data for testing
- ✅ Cascade delete for data integrity
- ✅ Timestamps for audit trail

#### DevOps
- ✅ Docker Compose orchestration
- ✅ Multi-container setup (backend, frontend, database, nginx)
- ✅ Health checks for service monitoring
- ✅ Environment-based configuration

#### Documentation
- ✅ Comprehensive README.md
- ✅ API Documentation
- ✅ Setup instructions (Docker & development)
- ✅ Deployment guide
- ✅ Contributing guidelines
- ✅ Technology stack documentation

### Infrastructure
- Flask 3.0.0
- React 18.2.0
- Vite 5.2.8
- PostgreSQL 16
- Docker & Docker Compose
- Nginx for reverse proxy

## [Unreleased]

The planned work is grouped by implementation priority; no release dates are
implied. See the [project roadmap](README.md#roadmap) for descriptions.

### Foundation and reliability
- [ ] Unit, integration, and end-to-end tests
- [ ] Logging system and enhanced error messages
- [ ] Input sanitization, SQL injection prevention, and XSS protection
- [ ] CSRF protection, security headers, and HTTPS enforcement
- [ ] API rate limiting and dependency vulnerability scanning
- [ ] Database query optimization and performance monitoring
- [ ] Caching layer (Redis)

### Personal productivity
- [ ] Search functionality
- [ ] Categories and tags for checklists
- [ ] Due dates and reminders
- [ ] Recurring checklists
- [ ] Templates library
- [ ] Export to PDF and Excel
- [ ] Dark mode

### Accounts and collaboration
- [ ] User authentication and authorization
- [ ] Checklist sharing and collaboration
- [ ] Comments on items
- [ ] Activity logging
- [ ] Email notifications

### Integrations and platforms
- [ ] Webhook support
- [ ] Native mobile apps

---

## Legend

### Categories
- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security-related changes

### Icons
- ✅ Implemented and tested
- 🔄 In progress
- 📋 Planned
- ⚠️ Deprecated
- 🐛 Bug fix

---

## How to Contribute Changes

1. Create a branch from `main`
2. Make your changes
3. Test thoroughly
4. Update this file under "Unreleased" section
5. Create a pull request
6. Upon release, move items from "Unreleased" to the appropriate version section

## Release Schedule

- **Patch versions** (1.0.x): Bug fixes and minor improvements - as needed
- **Minor versions** (1.x.0): New features - monthly
- **Major versions** (x.0.0): Breaking changes - as needed

---

For more information, see [CONTRIBUTING.md](CONTRIBUTING.md)
