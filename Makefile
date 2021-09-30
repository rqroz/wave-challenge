setup:
	virtualenv -p python3.6 .venv
	.venv/bin/pip install -r requirements/common.txt

run:
	(source .venv/bin/activate && scripts/run.sh)

test:
	(source .venv/bin/activate && scripts/test.sh)
