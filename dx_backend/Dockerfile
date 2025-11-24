FROM python:3.11-slim

WORKDIR /application

# Install system dependencies including curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY ./apps apps
COPY ./dx_backend dx_backend
COPY ./templates templates
COPY /manage.py manage.py
COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system --deploy

# Expose the port used by Gunicorn
ENV DJANGO_SETTINGS_MODULE=dx_backend.settings

CMD ["daphne", "dx_backend.asgi:application", "--port", "8000"]

EXPOSE 8000