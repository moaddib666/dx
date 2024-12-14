FROM python:3.11-slim

WORKDIR /application

COPY ./apps apps
COPY ./dx_backend dx_backend
COPY /manage.py manage.py
COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock

RUN pip install pipenv \
    && pipenv sync
# use daphne as ASGI server
ENV DJANGO_SETTINGS_MODULE=dx_backend.settings

CMD ["daphne", "dx_backend.asgi:application", "--port", "8080"]

EXPOSE 8080