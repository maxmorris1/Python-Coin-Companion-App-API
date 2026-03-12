# Docker Quick Start Guide

## Prerequisites

- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))
- Docker Compose (comes with Docker Desktop)

## Quick Start

1. **Navigate to the API directory:**
   ```bash
   cd API
   ```

2. **Build and start the container:**
   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## Common Commands

### Start the API (background)
```bash
docker-compose up -d
```

### Stop the API
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Rebuild after code changes
```bash
docker-compose up --build
```

### Restart the container
```bash
docker-compose restart
```

### Execute commands inside the container
```bash
docker-compose exec api bash
```

## Troubleshooting

### Port 8000 already in use
Stop the conflicting process or change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Changed from 8000:8000
```

### Container won't start
Check logs:
```bash
docker-compose logs api
```

### Chrome/Selenium issues
The container includes Google Chrome and all necessary dependencies. If you encounter issues:
1. Ensure `shm_size: 2gb` is set in docker-compose.yml
2. Check that `SYS_ADMIN` capability is added

### Code changes not reflecting
The API uses `--reload` mode, so changes should be automatic. If not:
```bash
docker-compose restart
```

## File Structure

```
API/
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore          # Files excluded from Docker build
├── api.py                 # FastAPI application
├── coin_scraper.py        # Scraping logic
├── requirements.txt       # Python dependencies
└── ...
```

## Environment Variables

You can customize the API by setting environment variables in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - CHROME_BIN=/usr/bin/google-chrome
  - API_KEY=your_key_here  # Example
```

## Production Deployment

For production, modify `docker-compose.yml`:

1. Remove `--reload` flag
2. Remove volume mounts
3. Set appropriate restart policy
4. Add environment-specific configurations

Example production command:
```yaml
command: uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```
