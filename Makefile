setup:
	virtualenv -p python3.6 .venv
	.venv/bin/pip install -r requirements/dev.txt

run:
	scripts/run.sh
