APP_NAME="wave-app"

setup:
	virtualenv -p python3.6 .venv
	.venv/bin/pip install -r requirements/common.txt

run:
	(source .venv/bin/activate && scripts/run.sh)

test:
	(source .venv/bin/activate && scripts/test.sh)

docker-build:
	docker image rmi -f ${APP_NAME}:latest || true;
	docker build . -t ${APP_NAME}:latest
	docker tag ${APP_NAME}:latest ${APP_NAME}:$$(git rev-parse HEAD)

docker-run:
	-docker stop ${APP_NAME}
	docker run \
		-d --rm --name ${APP_NAME} \
		--env LOG_LEVEL \
		--env ENVIRONMENT \
		--env SECRET_KEY \
		--env DB_HOST \
		--env DB_PORT \
		--env DB_NAME \
		--env DB_USER \
		--env DB_PASS \
		--network=host \
		${APP_NAME}
