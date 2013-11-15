test:
	django-admin.py test --settings=djgpa.test_settings djgpa
coverage:
	export DJANGO_SETTINGS_MODULE=djgpa.test_settings && \
	coverage run --branch --source=djgpa `which django-admin.py` test djgpa && \
	coverage report --omit="djgpa/test*,djgpa/migrations/*,djgpa/management/*"
sphinx:
	cd docs && sphinx-build -b html -d .build/doctrees . .build/html
