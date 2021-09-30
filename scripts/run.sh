#!/bin/bash

if [ "${ENVIRONMENT:=development}" = "development" ]; then
  python run.py
else
  gunicorn -c gunicorn.conf.py run:server
fi
