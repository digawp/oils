all: setup_dev

bundle:
	node_modules/.bin/webpack --watch

hotreload:
	node utils/server.js

collect:
	node_modules/.bin/webpack
	django-admin.py collectstatic

shell:
	django-admin.py shell_plus

initial_data:
	django-admin.py loaddata classification_type identifier_type initial_role

db:
	django-admin.py migrate

more_data: db initial_data
	django-admin.py loaddata initial_user initial_patron location

dump:
	django-admin.py dumpdata patron --indent=4 > patron/fixtures/initial_patron.json
	django-admin.py dumpdata catalog.role --indent=4 > catalog/fixtures/initial_role.json


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
