.PHONY: test lint format

test:
	pytest -v

lint:
	flake8 src tests

format:
	black src tests
