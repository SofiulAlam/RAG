# Setup Guide - AI App Builder

This guide will help you set up and run the AI App Builder locally.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Docker & Docker Compose** (Recommended)
   - Docker: https://docs.docker.com/get-docker/
   - Docker Compose: https://docs.docker.com/compose/install/

2. **OR Local Development Tools**
   - Node.js 20+ and npm: https://nodejs.org/
   - Python 3.11+: https://www.python.org/downloads/
   - PostgreSQL 15+: https://www.postgresql.org/download/
   - Redis 7+: https://redis.io/download

3. **API Keys**
   - Anthropic API Key: https://console.anthropic.com/

## Option 1: Docker Setup (Recommended)

### Step 1: Clone and Configure

```bash
# Clone the repository
git clone <repository-url>
cd ai-app-builder

# Set up backend environment
cd backend
cp .env.example .env
```

### Step 2: Edit Backend .env File

Open `backend/.env` and add your API keys:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Database (Docker will use these defaults)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/ai_app_builder

# Redis (Docker will use these defaults)
REDIS_URL=redis://redis:6379/0

# JWT (generate a secure key)
SECRET_KEY=your-secret-key-here-change-this

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

### Step 3: Set up Frontend Environment

```bash
# Go to frontend directory
cd ../frontend
cp .env.local.example .env.local
```

The default values should work:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Step 4: Start Services

```bash
# From the root directory
cd ..
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 5: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Useful Docker Commands

```bash
# Stop services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Rebuild services
docker-compose up -d --build

# View logs for a specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh
```

## Option 2: Local Development Setup

### Step 1: Set Up PostgreSQL

```bash
# Create database
createdb ai_app_builder

# Or using psql
psql -U postgres
CREATE DATABASE ai_app_builder;
\q
```

### Step 2: Set Up Redis

```bash
# Start Redis (macOS with Homebrew)
brew services start redis

# Or using Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### Step 3: Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Start the server
python main.py
```

The backend should now be running at http://localhost:8000

### Step 4: Set Up Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.local.example .env.local

# Start development server
npm run dev
```

The frontend should now be running at http://localhost:3000

## Verifying Installation

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### 2. Check API Documentation

Visit http://localhost:8000/docs to see the interactive API documentation.

### 3. Test Prompt Enhancement

```bash
curl -X POST http://localhost:8000/api/prompts/enhance \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Build a todo app"}'
```

### 4. Open Frontend

Visit http://localhost:3000 and you should see the landing page.

## Troubleshooting

### Backend Issues

**Database connection error**
```bash
# Check PostgreSQL is running
docker-compose ps postgres
# OR
psql -U postgres -c "SELECT version();"

# Check connection string in .env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
```

**Redis connection error**
```bash
# Check Redis is running
docker-compose ps redis
# OR
redis-cli ping
# Should return: PONG
```

**Anthropic API error**
```bash
# Verify your API key in backend/.env
ANTHROPIC_API_KEY=sk-ant-...

# Test API key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'
```

### Frontend Issues

**Module not found**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**API connection error**
```bash
# Check NEXT_PUBLIC_API_URL in .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# Verify backend is running
curl http://localhost:8000/health
```

### Docker Issues

**Port already in use**
```bash
# Check what's using the port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL

# Kill the process or change ports in docker-compose.yml
```

**Database initialization fails**
```bash
# Remove volumes and restart
docker-compose down -v
docker-compose up -d

# Check logs
docker-compose logs postgres
```

## Database Migrations

### Creating a New Migration

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Review the generated migration in alembic/versions/

# Apply the migration
alembic upgrade head
```

### Rolling Back Migrations

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all
alembic downgrade base
```

## Development Workflow

### 1. Starting Development

```bash
# With Docker
docker-compose up -d

# Without Docker
# Terminal 1: Backend
cd backend && source venv/bin/activate && python main.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

### 2. Making Changes

- **Backend**: Changes auto-reload with `--reload` flag
- **Frontend**: Changes auto-reload with Next.js Fast Refresh
- **Database Models**: Create migration with Alembic

### 3. Testing Changes

```bash
# Backend tests
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test

# Type checking
cd frontend
npm run type-check
```

### 4. Code Formatting

```bash
# Backend (Black)
cd backend
black .

# Frontend (Prettier - if configured)
cd frontend
npm run format
```

## Production Deployment

### Environment Variables

Update these for production:

**Backend**
```bash
ENVIRONMENT=production
SECRET_KEY=<generate-strong-random-key>
DATABASE_URL=<production-database-url>
REDIS_URL=<production-redis-url>
ALLOWED_ORIGINS=https://your-domain.com
```

**Frontend**
```bash
NEXT_PUBLIC_API_URL=https://api.your-domain.com
NEXT_PUBLIC_WS_URL=wss://api.your-domain.com
```

### Database

```bash
# Run migrations on production
alembic upgrade head

# Backup database
pg_dump -U postgres ai_app_builder > backup.sql
```

### Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Use HTTPS for all connections
- [ ] Set up proper CORS origins
- [ ] Enable rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular database backups
- [ ] Keep dependencies updated

## Next Steps

1. **Read the README.md** for feature documentation
2. **Explore the API** at http://localhost:8000/docs
3. **Create your first project** in the dashboard
4. **Try prompt enhancement** to see AI in action
5. **Check the Development Roadmap** to see what's coming

## Getting Help

- **Issues**: Create an issue on GitHub
- **Questions**: Check existing issues or create a discussion
- **Documentation**: See README.md and inline code comments

Happy coding! 🚀
