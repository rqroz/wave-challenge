setup:
	virtualenv -p python3.6 .venv
	.venv/bin/pip install -r requirements/common.txt

run:
	(source .venv/bin/activate && scripts/run.sh)

test:
	(source .venv/bin/activate && scripts/test.sh)

docker-build:
	docker image rmi -f wave-app:latest || true;
	docker build . -t wave-app:latest
	docker tag wave-app:latest wave-app:$$(git rev-parse HEAD)

docker-run-dev:
	-docker stop wave-app
	docker run -d --rm --name wave-app --network=host wave-app
