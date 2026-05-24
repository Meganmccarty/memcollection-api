include .env
export

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | \
	awk 'BEGIN {FS = ":.*?## "; OFS = ""} \
	{comment = $$2; \
	printf "\033[36m%-30s\033[0m", $$1; \
	line = ""; \
	while (length(comment) > 60) { \
		split(comment, parts, " "); \
		line = ""; \
		for (i = 1; i <= length(parts); i++) { \
			if (length(line " " parts[i]) > 60) { \
				printf " %s\n%-30s", line, ""; \
				line = parts[i]; \
			} else { \
				line = (line == "" ? parts[i] : line " " parts[i]); \
			} \
		} \
		comment = line; \
	} \
	printf " %s\n", comment; }'

# Docker commands
build: ## Builds Docker containers for the Wagtail app and Postgres database
	docker compose build

build-no-cache: ## Builds Docker containers without caching
	docker compose build --no-cache

up: ## Builds and runs Docker containers for the Wagtail app and database
	docker compose up

down: ## Tears down the Docker containers
	docker compose down

prune: ## Prunes Docker system, containers, mages, and volumes
	docker system prune; docker container prune; docker image prune; docker volume prune

# Docker commands for M chip Macs
mac-build: ## Builds Docker containers for the Wagtail app and Postgres database for M chip Macs
	docker compose -f docker-compose.yaml -f docker-compose.mac-m.yaml build

mac-build-no-cache: ## Builds Docker containers without caching for M chip Macs
	docker compose -f docker-compose.yaml -f docker-compose.mac-m.yaml build --no-cache

mac-up: ## Builds and runs Docker containers for the Wagtail app and database for M chip Macs
	docker compose -f docker-compose.yaml -f docker-compose.mac-m.yaml up

# Wagtail commands
makemigrations: ## Makes migrations of the Wagtail app within the Docker container
	docker compose run --rm web python manage.py makemigrations

migrate: ## Migrates the database of the Wagtail app within the Docker container
	docker compose run --rm web python manage.py migrate

update-index: ## Updates the Wagtail search index
	docker compose run --rm web python manage.py update_index

rebuild-ref-index: ## Rebuilds the Wagtail reference index (for when data is added or edited outside of Wagtail)
	docker compose run --rm web python manage.py rebuild_references_index

createsuperuser: ## Creates a super user for the Wagtail app
	docker compose run --rm web python manage.py createsuperuser

create-app: ## Creates new Django app (must set 'name=YOUR-APP-NAME')
	docker compose run --rm web python manage.py startapp $(name)

create-species-pages: ## Creates species pages for each species in the database (only creates pages for species that are missing them)
	docker compose run --rm web python manage.py create_species_pages

# Data fixture commands
dumpdata: ## Creates a JSON fixture from data in the database (must set 'model=app.Model' and 'output=app/fixtures/models.json')
	docker compose run --rm web python manage.py dumpdata $(model) --output=$(output) --indent=4 --natural-foreign

loaddata: ## Loads data from fixtures into the database (must set 'model=models.json')
	docker compose run --rm web python manage.py loaddata $(model)

load-fixtures: ## Loads all fixture data into the database
	docker compose run --rm web python manage.py loaddata countries.json states.json counties.json localities.json \
		gps_coordinates.json collecting_trips.json orders.json families.json subfamilies.json tribes.json genera.json \
		species.json subspecies.json people.json specimen_records.json

# Database backup and restore commands
DB_NAME := ${DATABASE_NAME}
DB_USER := ${DATABASE_USER}
PGPASSWORD := ${DATABASE_PASSWORD}

full-local-backup: ## Creates a full/complete local Postgres backup
	docker compose exec -T db \
	pg_dump --format=custom -v --no-owner --no-acl \
	-U $(DB_USER) -d $(DB_NAME) \
	> db_backups/$$(date +'%Y%m%d%H%M%S_local.backup')

verify-backup: ## Verifies that the backup was successful (must set 'filename=path/to/file.backup')
	docker compose exec -T db \
	pg_restore --list $(filename)

full-local-restore: ## Restores a full/complete local Postgres backup (must set 'filename=path/to/file.backup')
	docker compose exec -T \
	-e PGPASSWORD=$(PGPASSWORD) \
	db \
	pg_restore -v --no-owner --no-acl --clean \
	-h db -U $(DB_USER) -d $(DB_NAME) \
	$(filename)

full-prod-backup: ## Creates a full/complete Postgres backup from the production database (must set 'dbname="prod-db-name"')
	pg_dump --format=custom -v --no-owner --no-acl \
	-d "$(dbname)" \
	-f db_backups/$$(date +'%Y%m%d%H%M%S_prod.backup')

full-prod-restore: ## Restores a full/complete Postgres backup to the production database (must set 'dbname="prod-dbname"' and 'filename=path/to/file.back')
	pg_restore -v -d "$(dbname)" $(filename)

get-b2-backup: ## Restores a prod backup from Backblaze B2 to the local database (must set 'bucket-name=<bucket-name>', 'filename=<path>/<to>/<file>/<filename>', 'new-filename=<new-filename>', 'url=<endpoint-url>', 'region=<region-bucket-is-in>', and 'profile=<name-of-aws-profile>')
	aws s3 cp s3://${bucket-name}/${filename} ./db_backups/${new-filename} --endpoint-url ${url} --region ${region} --profile ${profile}

local-backup: ## Creates a JSON backup of the local database (but only of my models)
	docker compose run --rm web python manage.py dumpdata geography specimens taxonomy > \
	"$$(date +'backup_local_memcollection_%F-%T.json')" --indent=4 --natural-foreign

local-restore: ## Loads a backup's data into the local database (must set 'filename=<filename>.json')
	docker compose run --rm web python manage.py loaddata $(filename)

# Linting, formatting, and testing commands
lint: ## Lints Python code using flake8
	docker compose run --rm web python -m flake8 .

format: ## Formats Python code using Black formatter
	docker compose run --rm web python -m black .

test: ## Tests Python code
	docker compose run --rm web coverage run manage.py test --verbosity=2 --pattern="test_*.py"

test-deprecation: ## Tests Python code and includes deprecation warnings
	docker compose run --rm web python -Wa manage.py test

coverage: ## Shows test coverage
	docker compose run --rm web coverage report -m --omit=*/migrations/*,*/tests/*

# Deploy commands
fly-auth: ## Authenticates to Fly.io
	fly auth login

fly-secrets: ## Sets up Fly.io to use the .env.production secrets file
	flyctl secrets import < .env.production

fly-deploy: ## Deploys to Fly.io
	make fly-secrets && \
	fly deploy --ha=false

fly-run-command: ## Runs a command on the live deployed Fly app (must set command='your-command-here')
	flyctl ssh console -C "${command}"

# Doc and changelog commands
build-changelog: ## Builds an updated changelog
	npm run changelog

build-docs: ## Builds the Sphinx docs as static HTML files
	docker compose run --rm web sphinx-build -M html docs/source/ docs/build/
