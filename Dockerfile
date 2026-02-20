FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.4

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --without dev

COPY . .

EXPOSE 8000

CMD ["bash", "-lc", "python manage.py migrate && gunicorn LOL.wsgi:application --bind 0.0.0.0:8000"]
