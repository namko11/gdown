SHELL := /bin/bash

test:
	py.test

test-deps:
	pip install -r requirements.txt

six:
	python test_gdown.py

deps: requests
