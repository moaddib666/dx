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

#api-test:
#	curl  http://localhost:8000/api/schema/?format=json -o openapi.json
#		uvx schemathesis run openapi.json -u http://localhost:8000/api/ \
#		--header="Authorization: Bearer $(API_TOKEN)" \
#		--header="Accept: application/json" \
#		--wait-for-schema 5 \
#		--max-examples 2 \
#		--max-response-time 10 \
#		--request-timeout 15 \
#		--continue-on-failure \
#		-w 30 \
#		--checks=not_a_server_error,status_code_conformance,response_schema_conformance \
#		--suppress-health-check=too_slow,data_too_large \
#		--generation-deterministic \
#		--no-shrink \
#		--report=junit,har,vcr \
#		--report-dir=./test-reports \
#		--include-path-regex '^/character/.*'
#		--exclude-path-regex=".*/action/next_cycle.*" \
#		--exclude-path-regex=".*/adapters.*" \
		#		--max-failures 5 \

api-test-fast:
	curl http://localhost:8000/api/schema/?format=json -o openapi.json
	uvx schemathesis run openapi.json -u http://localhost:8000/api/ \
	--header="Authorization: Bearer $(API_TOKEN)" \
	--header="Accept: application/json" \
	--max-examples 1 \
	--max-response-time 5 \
	--request-timeout 10 \
	--continue-on-failure \
	-w 10 \
	--checks=not_a_server_error \
	--suppress-health-check=too_slow,data_too_large,filter_too_much \
	--generation-deterministic \
	--no-shrink \
	--include-method GET
#
#api-test-smoke:
#	curl http://localhost:8000/api/schema/?format=json -o openapi.json
#	uvx schemathesis --config-file schemathesis-smoke-test-config.toml \
# 		run openapi.json \
# 		-u http://localhost:8000/api/ \
#		--header="Authorization: Bearer $(API_TOKEN)" \
#		--max-examples 1 \
#		-w 5 \
#		--checks=not_a_server_error \
#		--suppress-health-check=too_slow,data_too_large,filter_too_much \
#		--generation-deterministic \
#		--no-shrink
