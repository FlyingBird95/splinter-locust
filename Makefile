SHELL := /bin/bash

develop: env python-deps pre-commit-hooks

env:
	-rm -rf .env/bin/python* .env/bin/pip*
	virtualenv .env

python-deps:
	env pip3 install -e .[dev]

pre-commit-hooks:
	env pre-commit install
	env pre-commit install-hooks

run:
	locust --host http://localhost:5000 --headless --run-time 20s
