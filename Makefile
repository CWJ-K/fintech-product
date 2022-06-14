
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
	