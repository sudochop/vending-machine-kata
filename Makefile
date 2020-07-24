develop: format lint typecheck test test container

format:
	pipenv run black .
	pipenv run isort .

lint:
	pipenv run flake8 .

typecheck:
	pipenv run mypy .

test:
	pipenv run pytest -vv  .
	pipenv run pytest --cov --cov-fail-under=100 --cov-report term-missing

container:
	docker-compose up