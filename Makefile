.PHONY: f1
all: setup_dev

DJANGO_CMD=./manage.py
PROJECT_NAME={{ project_name }}

bundle:
	node_modules/.bin/webpack --watch

collect:
	node_modules/.bin/webpack
	$(DJANGO_CMD) collectstatic

shell:
	$(DJANGO_CMD) shell_plus

initial_data:
	$(DJANGO_CMD) loaddata classification_type identifier_type initial_role

tbl_data: demo
	$(DJANGO_CMD) load_tbl

db:
	$(DJANGO_CMD) migrate

demo: db initial_data
	$(DJANGO_CMD) loaddata initial_user initial_patron initial_location

dump:
	$(DJANGO_CMD) dumpdata patron --indent=4 > {{ project_name }}/fixtures/initial_patron.json

# DEVELOPMENT
dev_env:
	$(eval export DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).settings.dev)

reset_dev_db:
	-dropdb $(PROJECT_NAME)_dev
	createdb $(PROJECT_NAME)_dev

setup_dev: dev_env
	npm install
	pip install -r requirements/dev.pip
	-createdb $(PROJECT_NAME)_dev
	$(MAKE) db initial_data

dev: dev_env
	$(DJANGO_CMD) runserver 0.0.0.0:8000


# PRODUCTION
prod_env:
	$(eval export DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).settings.prod)

setup_prod: prod_env
	npm install
	pip install -r requirements/prod.pip
	-createdb $(PROJECT_NAME)
	$(MAKE) db initial_data collect

prod: prod_env
	$(DJANGO_CMD) runserver 0.0.0.0:8000


# TESTING
test_env:
	$(eval export DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).settings.test)

setup_test: test_env
	npm install
	pip install -r requirements/test.pip
	-dropdb $(PROJECT_NAME)_test
	createdb $(PROJECT_NAME)_test
	$(MAKE) db initial_data

test: test_env
	coverage run --source='.' $(DJANGO_CMD) test
