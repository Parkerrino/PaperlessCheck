# Deployment & CI/CD Guide

## CI/CD Pipelines

GitHub Actions setup:
- **CI** (`ci.yml`): Lint (ruff/black), pytest, npm build, Docker integration (DB init + health).
- **Docker Build/Push** (`docker-build-push.yml`): GHCR images on tags/releases.
- **Dependabot**: Weekly dep updates.

Push/PR to `main/develop` triggers CI.

## Production Deployment

## Prerequisites

- Docker and Docker Compose installed
- Domain name (for production)
- SSL certificate (recommended)
- PostgreSQL backup strategy in place

## Production Deployment

### 1. Environment Configuration

Create a `.env.production` file:

```env
# Backend
DATABASE_URL=postgresql://paperless:SECURE_PASSWORD@db:5432/paperlesscheck
FLASK_ENV=production

# Security
DEBUG=False
```

### 2. Docker Compose Production Setup

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: paperlesscheck-backend
    environment:
      - DATABASE_URL=postgresql://paperless:${DB_PASSWORD}@db:5432/paperlesscheck
      - FLASK_ENV=production
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: always

  frontend:
    build: ./frontend
    container_name: paperlesscheck-frontend
    depends_on:
      - backend
    restart: always

  db:
    image: postgres:16
    container_name: paperlesscheck-db
    environment:
      - POSTGRES_USER=paperless
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=paperlesscheck
    volumes:
      - paperlesscheck_db_data:/var/lib/postgresql/data
      - ./database/init.sql/:/docker-entrypoint-initdb.d/
    restart: always

  nginx:
    image: nginx:alpine
    container_name: paperlesscheck-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
    restart: always

volumes:
  paperlesscheck_db_data:
```

### 3. Nginx SSL Configuration

Create `nginx.prod.conf`:

```nginx
upstream backend {
    server backend:5000;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Deploy

```bash
# Generate SSL certificates (e.g., using Let's Encrypt with Certbot)
certbot certonly --standalone -d yourdomain.com

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Database Backup Strategy

### Regular Backups

```bash
#!/bin/bash
# backup.sh - Run daily via cron

BACKUP_DIR="/backups/paperlesscheck"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONTAINER="paperlesscheck-db"

mkdir -p $BACKUP_DIR

docker exec $CONTAINER pg_dump -U paperless paperlesscheck | \
  gzip > $BACKUP_DIR/backup_$TIMESTAMP.sql.gz

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/backup_$TIMESTAMP.sql.gz"
```

### Restore from Backup

```bash
gunzip < backup_TIMESTAMP.sql.gz | \
  docker exec -i paperlesscheck-db psql -U paperless paperlesscheck
```

## Monitoring

### Health Checks

```bash
# Check backend health
curl https://yourdomain.com/api/health

# Check database
docker-compose exec db psql -U paperless -d paperlesscheck -c "SELECT 1;"
```

### Log Monitoring

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

## Updates

### Update to Latest Version

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose -f docker-compose.prod.yml build --no-cache

# Restart services
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Verify health
curl https://yourdomain.com/api/health
```

## Troubleshooting

### Container Not Starting

```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Database Connection Issues

```bash
# Test database connection
docker-compose exec backend python -c \
  "import psycopg2; psycopg2.connect(os.getenv('DATABASE_URL'))"
```

### SSL Certificate Issues

```bash
# Check certificate validity
openssl x509 -in ssl/cert.pem -text -noout

# Renew Let's Encrypt certificate
certbot renew

# Copy new certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem

# Restart nginx
docker-compose restart nginx
```

## Performance Optimization

- Enable gzip compression in Nginx
- Configure CDN for static assets
- Implement database query optimization
- Set up Redis caching for API responses
- Use horizontal scaling with load balancer

## Security Hardening

- Keep all containers updated
- Use strong database passwords
- Implement rate limiting
- Enable CORS restrictions
- Regular security audits
- Monitor for vulnerabilities
