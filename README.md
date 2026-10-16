# Project 3: Full-Stack SaaS with DevOps & DevSecOps

## Overview
A complete SaaS application demonstrating DevOps and DevSecOps best practices.

**Stack:**
- Frontend: React 18
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Container Orchestration: Kubernetes (k3d)
- Infrastructure: Terraform + AWS
- CI/CD: GitHub Actions

## Quick Start

### Prerequisites
- Docker
- k3d
- kubectl
- Python 3.13
- Node.js 18

### Run Locally

```bash
# Terminal 1: Start k3d cluster
k3d cluster create dev

# Terminal 2: Port-forward PostgreSQL
kubectl port-forward -n databases svc/postgres 5432:5432

# Terminal 3: Port-forward Backend
kubectl port-forward -n apps svc/backend 8000:80

# Terminal 4: Port-forward Frontend
kubectl port-forward -n apps svc/frontend 3000:80

# Terminal 5: Run migrations & tests
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
pytest test_api.py -v

# Visit http://localhost:3000
```

## Architecture

[Include diagram here if possible]

- **Frontend:** React SPA served by Nginx
- **Backend:** FastAPI with SQLAlchemy ORM
- **Database:** PostgreSQL with Alembic migrations
- **Orchestration:** Kubernetes manifests for all services

## DevSecOps Practices

✅ Dependency scanning (safety, npm audit)
✅ Container image scanning (trivy)
✅ Secrets management (Kubernetes secrets, GitHub secrets)
✅ Automated testing (pytest, GitHub Actions)
✅ Infrastructure as Code (Terraform)

## Known gaps (learning build, not production)
- JWT SECRET_KEY is hardcoded in backend/app/main.py
- Passwords are stored in plaintext (no hashing yet)
- Database password "devpassword" appears in k3d manifests

## CI/CD Pipeline

Push to main → GitHub Actions:
1. Run dependency scans
2. Run API tests
3. Scan container images
4. Build Docker images
5. Ready for deployment

## Deployment to AWS

See DEPLOYMENT.md

## What I Learned

- Kubernetes internals & k3d
- Infrastructure as Code (Terraform)
- CI/CD automation (GitHub Actions)
- Database migrations (Alembic)
- Security practices (DevSecOps)
- Full-stack development

## Next Steps

- [ ] Deploy to AWS ECS/EKS
- [ ] Add authentication (JWT improvements)
- [ ] Add authorization (role-based access)
- [ ] Add API rate limiting
- [ ] Add monitoring (CloudWatch/Prometheus)
