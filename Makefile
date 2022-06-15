GIT_TAG := $(shell git describe --abbrev=0 --tags)

build-image:
	docker build -f Dockerfile -t louisekr/crawler:${GIT_TAG} .

push-image:
	docker push louisekr/crawler:${GIT_TAG}

deploy-crawler:
	GIT_TAG=${GIT_TAG} docker stack deploy --with-registry-auth -c crawler.yml financialdata

deploy-scheduler:
	GIT_TAG=$(GIT_TAG) docker stack deploy --with-registry-auth -c scheduler.yml financialdata

create-mysql:
	docker-compose -f mysql.yml up -d

create-rabbitmq:
	docker-compose -f rabbitmq.yml up -d

install-python-env:
	pipenv sync

run-celery-twse:
	pipenv run celery -A src.tasks.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q twse_crawler

sent-taiwan-stock-price-task:
	pipenv run python src/producer.py twse_crawler 2021-04-01 2021-04-12

gen-dev-env-variable:
	python genenv.py

	VERSION=STAGING python genenv.py

gen-release-env-variable:
	VERSION=RELEASE python genenv.py

run-scheduler:
	pipenv run python scheduler.py
	