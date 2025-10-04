# AirAware Deployment Guide

This guide provides comprehensive instructions for deploying the AirAware application in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Configuration](#configuration)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **Memory**: Minimum 8GB RAM (16GB recommended for production)
- **Storage**: Minimum 50GB free space
- **CPU**: 4+ cores recommended

### Software Requirements

- **Docker**: 20.10+ with Docker Compose 2.0+
- **Python**: 3.11+ (for local development)
- **Node.js**: 18+ (for frontend development)
- **PostgreSQL**: 15+ with PostGIS extension
- **Redis**: 7+

### API Keys Required

- **AirNow API Key**: [Register here](https://www.airnowapi.org/)
- **NASA Earthdata Account**: [Register here](https://urs.earthdata.nasa.gov/)
- **Mapbox Token**: [Get token here](https://www.mapbox.com/)
- **SendGrid API Key**: [Optional, for email notifications](https://sendgrid.com/)
- **Twilio Credentials**: [Optional, for SMS notifications](https://www.twilio.com/)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd NASA
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

Fill in your API keys and configuration:

```env
# Required API Keys
AIRNOW_API_KEY=your_airnow_api_key_here
NASA_EARTHDATA_USERNAME=your_nasa_username_here
NASA_EARTHDATA_PASSWORD=your_nasa_password_here
MAPBOX_TOKEN=your_mapbox_token_here

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/airaware

# Redis
REDIS_URL=redis://localhost:6379
```

### 3. Start Development Environment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

### 5. Initialize Database

```bash
# Run database migrations
docker-compose exec backend python -c "from app.core.database import init_db; init_db()"

# Load sample data
docker-compose exec backend python scripts/load_sample_data.py
```

## Docker Deployment

### Production Docker Compose

Create a production configuration:

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgis/postgis:15-3.3
    environment:
      POSTGRES_DB: airaware
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: ../Dockerfile.backend
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/airaware
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: ../Dockerfile.frontend
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

### Deploy to Production

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d

# Scale services if needed
docker-compose -f docker-compose.prod.yml up -d --scale celery-worker=3
```

## Cloud Deployment

### AWS Deployment

#### 1. EC2 Instance Setup

```bash
# Launch EC2 instance (t3.large or larger)
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu

# Clone repository
git clone <repository-url>
cd NASA
```

#### 2. RDS Database Setup

```bash
# Create RDS PostgreSQL instance with PostGIS
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/airaware
```

#### 3. ElastiCache Redis Setup

```bash
# Create ElastiCache Redis cluster
# Update REDIS_URL in .env
REDIS_URL=redis://your-elasticache-endpoint:6379
```

#### 4. Application Load Balancer

```bash
# Create ALB with SSL certificate
# Configure health checks on /health endpoint
# Set up auto-scaling groups
```

### Google Cloud Platform Deployment

#### 1. Google Kubernetes Engine (GKE)

```bash
# Create GKE cluster
gcloud container clusters create airaware-cluster \
    --num-nodes=3 \
    --machine-type=e2-standard-4 \
    --zone=us-central1-a

# Deploy application
kubectl apply -f k8s/
```

#### 2. Cloud SQL Setup

```bash
# Create Cloud SQL PostgreSQL instance
# Enable PostGIS extension
# Update connection string
```

### Azure Deployment

#### 1. Azure Container Instances

```bash
# Create resource group
az group create --name airaware-rg --location eastus

# Deploy container instances
az container create \
    --resource-group airaware-rg \
    --name airaware-backend \
    --image your-registry/airaware-backend:latest
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `REDIS_URL` | Redis connection string | Yes | - |
| `AIRNOW_API_KEY` | AirNow API key | Yes | - |
| `NASA_EARTHDATA_USERNAME` | NASA Earthdata username | Yes | - |
| `NASA_EARTHDATA_PASSWORD` | NASA Earthdata password | Yes | - |
| `MAPBOX_TOKEN` | Mapbox access token | Yes | - |
| `WEB_PUSH_VAPID_PUBLIC_KEY` | VAPID public key | No | - |
| `WEB_PUSH_VAPID_PRIVATE_KEY` | VAPID private key | No | - |
| `SENDGRID_API_KEY` | SendGrid API key | No | - |
| `TWILIO_ACCOUNT_SID` | Twilio account SID | No | - |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | No | - |

### Database Configuration

```sql
-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create indexes for performance
CREATE INDEX CONCURRENTLY idx_air_quality_stations_location 
ON air_quality_stations USING GIST (location);

CREATE INDEX CONCURRENTLY idx_air_quality_readings_timestamp 
ON air_quality_readings (timestamp);
```

### Redis Configuration

```conf
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

## Monitoring and Maintenance

### Health Checks

```bash
# Check application health
curl http://localhost:8000/health

# Check database connectivity
docker-compose exec backend python -c "from app.core.database import get_db; next(get_db())"

# Check Redis connectivity
docker-compose exec redis redis-cli ping
```

### Logging

```bash
# View application logs
docker-compose logs -f backend

# View specific service logs
docker-compose logs -f celery-worker

# View error logs only
docker-compose logs --tail=100 backend | grep ERROR
```

### Backup and Recovery

#### Database Backup

```bash
# Create backup
docker-compose exec postgres pg_dump -U postgres airaware > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker-compose exec -T postgres psql -U postgres airaware < backup_20240115_120000.sql
```

#### Automated Backups

```bash
# Add to crontab
0 2 * * * /path/to/backup_script.sh
```

### Performance Monitoring

```bash
# Monitor resource usage
docker stats

# Check database performance
docker-compose exec postgres psql -U postgres airaware -c "SELECT * FROM pg_stat_activity;"

# Monitor Redis
docker-compose exec redis redis-cli info memory
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

```bash
# Check database status
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

#### 2. Redis Connection Issues

```bash
# Check Redis status
docker-compose exec redis redis-cli ping

# Check Redis logs
docker-compose logs redis

# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

#### 3. API Key Issues

```bash
# Test AirNow API
curl "https://www.airnowapi.org/aq/observation/zipCode/query?format=application/json&zipCode=10001&API_KEY=YOUR_KEY"

# Test NASA Earthdata
curl -u "username:password" "https://asdc.larc.nasa.gov/data/TEMPO/"
```

#### 4. Frontend Build Issues

```bash
# Clear Next.js cache
docker-compose exec frontend rm -rf .next

# Rebuild frontend
docker-compose build --no-cache frontend
```

### Performance Optimization

#### 1. Database Optimization

```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM air_quality_readings WHERE timestamp > NOW() - INTERVAL '24 hours';

-- Update table statistics
ANALYZE air_quality_readings;

-- Vacuum database
VACUUM ANALYZE;
```

#### 2. Redis Optimization

```bash
# Monitor Redis memory usage
docker-compose exec redis redis-cli info memory

# Set memory limits
docker-compose exec redis redis-cli CONFIG SET maxmemory 2gb
```

#### 3. Application Optimization

```bash
# Monitor CPU and memory usage
docker stats

# Scale services
docker-compose up -d --scale celery-worker=3
```

### Security Considerations

#### 1. Environment Variables

```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use secrets management
docker secret create api_key ./api_key.txt
```

#### 2. Network Security

```bash
# Use internal networks
docker network create airaware-internal

# Restrict external access
docker-compose exec nginx nginx -t
```

#### 3. Database Security

```sql
-- Create read-only user
CREATE USER readonly_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE airaware TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
```

## Support and Resources

### Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [Docker Documentation](https://docs.docker.com/)

### Community Support

- [GitHub Issues](https://github.com/your-repo/issues)
- [Discord Community](https://discord.gg/your-invite)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/airaware)

### Professional Support

For enterprise deployments and professional support, contact:
- Email: support@airaware.com
- Phone: +1-555-AIRAWARE
- Website: https://airaware.com/support
