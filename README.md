# LOL

Django + Python + MySQL starter environment managed with Poetry, ready for Docker and Kubernetes.

## Stack
- Django application: `LOL`
- Database: MySQL (`LOLDB`)
- Dependency manager: Poetry
- Container support: Docker / Docker Compose
- Orchestration manifests: Kubernetes (`k8s/`)

## 1) Local Poetry setup
```bash
poetry install
cp .env.example .env
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Health endpoint:
- `http://127.0.0.1:8000/health/`

## 2) Docker Compose setup
```bash
cp .env.example .env
docker compose up --build
```

## 3) Kubernetes setup
Build image first, then apply manifests:
```bash
docker build -t lol-app:latest .
kubectl apply -f k8s/mysql.yaml
kubectl apply -f k8s/app.yaml
```

## Notes
- Update secrets before production use.
- The sample MySQL deployment uses `emptyDir`; switch to a persistent volume for real environments.
