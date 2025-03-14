.PHONY: run build test lint cover dependencies


run:
	poetry run run_bot

dependencies:
	poetry install

build:
	docker buildx build -t copycat_tgbot .

lint:
	black .
	isort .
	find . -type f -name '*.py' | xargs -I {} -n 1 autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports {}

test:
	CONFIG=unittest pytest --capture=no --log-cli-level=INFO

cover:
	pytest --cov=copycat_tgbot \
	--cov-report xml --cov-report term --cov-report html \
		-o junit_family=xunit2 --junitxml=test_report.xml