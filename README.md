# 📋 PaperlessCheck

A modern, digital checklist management application built with Flask, React, and PostgreSQL. Organize your tasks, projects, and workflows in one centralized place.

## Features

✨ **Core Features**
- 📝 Create and manage multiple checklists
- ✅ Add and check off items in each checklist
- 📊 Progress tracking (completed items count)
- 🗑️ Delete checklists and individual items
- 💾 Persistent storage with PostgreSQL
- 🎨 Modern, responsive UI

🏗️ **Architecture**
- **Backend**: Flask REST API with PostgreSQL
- **Frontend**: React with Vite
- **Database**: PostgreSQL 16
- **Deployment**: Docker & Docker Compose

## Project Structure

```
PaperlessCheck/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Backend container definition
│   ├── routes/
│   │   └── checklist_routes.py # API endpoints
│   ├── services/
│   │   └── validation_service.py # Input validation logic
│   └── data/
│       └── sample_checklists.py # Sample data
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── main.jsx          # React entry point
│   │   └── index.css         # Styling
│   ├── index.html            # HTML template
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── nginx.conf            # Nginx configuration
│   └── Dockerfile            # Frontend container definition
├── database/
│   └── init.sql/
│       └── schema.sql        # Database schema & sample data
└── docker-compose.yml        # Docker Compose orchestration
```

## Prerequisites

- Docker and Docker Compose installed
- Or: Python 3.12+, Node.js 22+, PostgreSQL 16

## Quick Start with Docker

### 1. Clone and Setup
```bash
git clone <repository-url>
cd PaperlessCheck
```

### 2. Start Services
```bash
docker-compose up -d
```

### 3. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Database**: localhost:5432

## Development Setup

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set DATABASE_URL=postgresql://paperless:paperless@localhost:5432/paperlesscheck
set FLASK_ENV=development

# Run the application
python app.py
```

The backend API will be available at `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run start

# Build for production
npm run build
```

The frontend will be available at `http://localhost:5173` (Vite default)

### Database Setup

If running without Docker, set up PostgreSQL:

```sql
-- Create database
CREATE DATABASE paperlesscheck;

-- Create user
CREATE USER paperless WITH PASSWORD 'paperless';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE paperlesscheck TO paperless;

-- Connect to database and run schema.sql
\c paperlesscheck
\i database/init.sql/schema.sql
```

## API Documentation

### Base URL
```
http://localhost:5000/api/checklists
```

### Endpoints

#### Health Check
```
GET /health
Response: { "status": "healthy", "database": "connected" }
```

#### Get All Checklists
```
GET /
Response: [
  {
    "id": 1,
    "title": "Project Setup",
    "description": "Initial setup",
    "created_at": "2024-05-04T10:00:00",
    "items": [...]
  }
]
```

#### Get Specific Checklist
```
GET /<checklist_id>
Response: { checklist details with items }
```

#### Create Checklist
```
POST /
Body: {
  "title": "New Checklist",
  "description": "Optional description"
}
Response: { newly created checklist }
Status: 201
```

#### Update Checklist
```
PUT /<checklist_id>
Body: {
  "title": "Updated Title",
  "description": "Updated description"
}
Response: { updated checklist }
```

#### Delete Checklist
```
DELETE /<checklist_id>
Response: { "message": "Checklist deleted successfully" }
```

#### Add Item to Checklist
```
POST /<checklist_id>/items
Body: {
  "title": "Task item",
  "order_index": 1
}
Response: { newly created item }
Status: 201
```

#### Update Item
```
PUT /items/<item_id>
Body: {
  "title": "Updated item",
  "completed": true,
  "order_index": 1
}
Response: { updated item }
```

#### Delete Item
```
DELETE /items/<item_id>
Response: { "message": "Item deleted successfully" }
```

## Database Schema

### checklists table
```sql
CREATE TABLE checklists (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### checklist_items table
```sql
CREATE TABLE checklist_items (
    id SERIAL PRIMARY KEY,
    checklist_id INTEGER NOT NULL REFERENCES checklists(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Environment Variables

### Backend (.env or docker-compose.yml)
```
DATABASE_URL=postgresql://paperless:paperless@db:5432/paperlesscheck
FLASK_ENV=development
```

### Database (docker-compose.yml)
```
POSTGRES_USER=paperless
POSTGRES_PASSWORD=paperless
POSTGRES_DB=paperlesscheck
```

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | Flask | 3.0.0 |
| Backend ORM/Driver | psycopg2 | 2.9.9 |
| CORS | Flask-CORS | 4.0.0 |
| Frontend Framework | React | 18.2.0 |
| Frontend Build | Vite | 5.2.8 |
| Database | PostgreSQL | 16 |
| Containerization | Docker | Latest |

## Docker Commands

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (careful - deletes data!)
docker-compose down -v

# Rebuild containers
docker-compose build --no-cache
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check DATABASE_URL environment variable
- Verify credentials in docker-compose.yml

### Frontend Can't Reach API
- Ensure nginx is configured correctly
- Check docker-compose networking
- Verify backend container is running

### Port Already in Use
```bash
# Find and stop the service using the port
# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :3000
kill -9 <PID>
```

## Features Implemented for MVP

✅ Full CRUD operations for checklists
✅ Full CRUD operations for checklist items
✅ Item completion tracking
✅ Progress visualization
✅ Responsive web UI
✅ REST API with proper error handling
✅ Database persistence
✅ Docker containerization
✅ Health check endpoint
✅ Input validation

## Future Enhancements

🔮 Planned Features
- User authentication & authorization
- Checklist sharing and collaboration
- Due dates and reminders
- Categories/tags for checklists
- Search functionality
- Dark mode
- Mobile app
- Export to PDF/Excel
- Recurring checklists
- Templates library

## Testing

### Manual Testing
1. Create a checklist with title and description
2. Add multiple items to the checklist
3. Check/uncheck items
4. Update checklist title
5. Delete items
6. Delete entire checklist
7. Verify progress counting

### API Testing with cURL
```bash
# Get all checklists
curl http://localhost:5000/api/checklists

# Create a checklist
curl -X POST http://localhost:5000/api/checklists \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "description": "Test description"}'

# Health check
curl http://localhost:5000/health
```

## Performance Considerations

- Database indexes on checklist_id for faster item queries
- Frontend pagination can be added for large checklist collections
- Backend caching can be implemented for frequently accessed checklists
- API rate limiting can be added for production

## Security Considerations

For production deployment:
- Add authentication and authorization
- Use environment variables for sensitive data
- Implement rate limiting
- Add input sanitization
- Enable HTTPS/SSL
- Implement CSRF protection
- Add request validation
- Use database transaction rollbacks on errors

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Happy organizing! 📝✨**
