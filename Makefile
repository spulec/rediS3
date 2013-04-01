SHELL := /bin/bash
.PHONY: benchmark

init:
	python setup.py develop
	pip install -r requirements.txt

test:
	rm -f .coverage
	nosetests --with-coverage ./tests/

benchmark:
	python benchmark/benchmark.py
