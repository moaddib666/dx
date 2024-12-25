FROM python:3.11-slim

WORKDIR /application

COPY ./apps apps
COPY ./dx_backend dx_backend
COPY /manage.py manage.py
COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system --deploy

# Expose the port used by Gunicorn
ENV DJANGO_SETTINGS_MODULE=dx_backend.settings

CMD ["daphne", "dx_backend.asgi:application", "--port", "8000"]

EXPOSE 8000