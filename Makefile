.PHONY: freeze mm run csu clean

freeze:
	pip freeze > requirements.txt

mm:
	python manage.py makemigrations
	python manage.py migrate

run:
	py manage.py runserver

twrun:
	python manage.py tailwind start
	
csu:
	py manage.py createsuperuser

clean:
	rm -rf ./*/migrations/00*.py
	rm -rf ./*/__pycache__/*
	rm -rf ./*/migrations/__pycache__/*.pyc