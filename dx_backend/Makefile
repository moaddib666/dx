re-init-migrations: remove-migrations migrations migrate load-fixtures

remove-migrations:
	find . -path "./apps/*/migrations/*.py" -not -name "__init__.py" -delete
migrations:
	python manage.py makemigrations
load-fixtures:
	python manage.py loaddata apps/*/fixtures/*.json
migrate:
	python manage.py migrate
remove-db:
	rm db.sqlite3
re-init-db: remove-db migrate load-fixtures
	python manage.py createsuperuser
redis:
	docker-compose up -d redis
gateway:
	docker-compose up -d gateway