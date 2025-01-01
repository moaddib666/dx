re-init-migrations: remove-migrations migrations migrate load-fixtures

apps=action adapters character client core currency effects fight gallery game items modificators school skills world

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
dumpdata:
	python manage.py dumpdata $(apps) --indent 2 -o backup/full_data_dump.$(shell date +%Y-%m-%d).json