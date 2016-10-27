all: setup_dev

bundle:
	node_modules/.bin/webpack --watch

hotreload:
	node utils/server.js

collect:
	node_modules/.bin/webpack
	python manage.py collectstatic

shell:
	python manage.py shell_plus

initial_data:
	python manage.py loaddata classification_type identifier_type initial_role

db:
	python manage.py migrate

more_data: db initial_data
	python manage.py loaddata initial_user initial_patron location

dump:
	python manage.py dumpdata patron --indent=4 > patron/fixtures/initial_patron.json
	python manage.py dumpdata catalog.role --indent=4 > catalog/fixtures/initial_role.json

# DEVELOPMENT
dev_env: $(eval export DJANGO_SETTINGS_MODULE=oils.settings.dev)

setup_dev: dev_env
	npm install
	pip install -r requirements/dev.pip
	$(MAKE) more_data

dev: dev_env
	python manage.py runserver 0.0.0.0:8000


# PRODUCTION
prod_env: $(eval export DJANGO_SETTINGS_MODULE=oils.settings.prod)

setup_prod: prod_env
	npm install
	pip install -r requirements/prod.pip
	$(MAKE) db initial_data collect

prod: prod_env
	python manage.py runserver 0.0.0.0:8000


# TESTING
test_env: $(eval export DJANGO_SETTINGS_MODULE=oils.settings.test)

setup_test: test_env
	npm install
	pip install -r requirements/test.pip
	-dropdb oils_test
	createdb oils_test
	$(MAKE) db initial_data

test: test_env
	coverage run --source='.' -m py.test
