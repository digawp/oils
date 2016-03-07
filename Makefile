run:
	python manage.py runserver 0.0.0.0:8000

shell:
	python manage.py shell_plus

loaddata:
	python manage.py loaddata sample

dep:
	pip install -r requirements.txt
