
# Center Project Scaffold

## Local setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DEBUG=1
python manage.py migrate
python manage.py runserver
```

## Docker
```bash
cp .env.example .env
docker compose up --build
```

- Docs: http://localhost:8000/api/docs/
- Health: http://localhost:8000/api/core/health/
