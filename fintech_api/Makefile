install-python-env:
	pipenv sync


gen-dev-env-variable:
	python genenv.py

gen-staging-env-variable:
	VERSION=STAGING python genenv.py


gen-release-env-variable:
	VERSION=RELEASE python genenv.py

build-image:
	docker build -f Dockerfile -t api:7.2.2 .

up-api:
	docker-compose -f api.yml up

tag-image:
	docker tag api:7.2.2 linsamtw/api:7.2.2

push-image:
	docker push linsamtw/api:7.2.2