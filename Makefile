setup:
	virtualenv -p python3.6 .venv
	.venv/bin/pip install -r requirements/common.txt

run:
	scripts/run.sh
