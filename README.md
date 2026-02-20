# LOL

Django + Python + MySQL starter environment managed with Poetry, ready for Docker and Kubernetes.

## Stack
- Django application: `LOL`
- Database: MySQL (`LOLDB`)
- Dependency manager: Poetry
- Container support: Docker / Docker Compose
- Orchestration manifests: Kubernetes (`k8s/`)

## User separation
- `InternalUser` table (internal system users)
- `Customer` table (customer users)
- Separate login pages:
  - Internal user: `/internal/login/`
  - Customer: `/customer/login/`
- Customers are created by internal users at `/internal/customers/create/`.
- After login, each user sees a page with large user-type text:
  - `INTERNAL USER`
  - `CUSTOMER`

Default seeded internal user (created by migration):
- Username: `internal_admin`
- Password: `internal_admin`

## 1) Local Poetry setup
```bash
poetry install
cp .env.example .env
poetry run python manage.py migrate
```

Alternative pip install:
```bash
pip install -r requirements.txt
```

Run on separate ports in two terminals:
```bash
poetry run python manage.py runserver 0.0.0.0:8000
poetry run python manage.py runserver 0.0.0.0:9000
```

> Note: TCP ports `80080` and `90080` are invalid (>65535), so the environment uses `8000` and `9000`.

## 2) Docker Compose setup
```bash
cp .env.example .env
docker compose up --build
```

Endpoints:
- Internal entry: `http://127.0.0.1:8000/`
- Customer entry: `http://127.0.0.1:9000/`

## 3) Kubernetes setup
Build image first, then apply manifests:
```bash
docker build -t lol-app:latest .
kubectl apply -f k8s/mysql.yaml
kubectl apply -f k8s/app.yaml
```

Services:
- Internal: `lol-app-internal:8000`
- Customer: `lol-app-customer:9000`

## Notes
- Update secrets before production use.
- The sample MySQL deployment uses `emptyDir`; switch to a persistent volume for real environments.
