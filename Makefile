.PHONY: run test doc lint cover dependencies


run:
	python ./copycat_tgbot/run.py

dependencies:
	poetry install

lint:
	black .
	isort .
	find . -type f -name '*.py' | xargs -I {} -n 1 autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports {}