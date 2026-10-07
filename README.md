# Project 3: SaaS Dashboard MVP

## Architecture
- **Frontend**: React 18 (localhost:3000)
- **Backend**: FastAPI (localhost:8000)
- **Database**: PostgreSQL 15 (k3d)
- **Container Orchestration**: Kubernetes (k3d)

## Features
- User registration & login with JWT
- Task management
- CORS-enabled API

## Running Locally
```bash
# Terminal 1: PostgreSQL port-forward
kubectl port-forward -n databases svc/postgres 5432:5432

# Terminal 2: Backend port-forward
kubectl port-forward -n apps svc/backend 8000:80

# Terminal 3: Frontend dev server
cd frontend && npm start
```

Visit http://localhost:3000

## What's Next
- CI/CD pipeline (GitHub Actions)
- Monitoring & logs (CloudWatch)
- Production deployment (AWS)