build:
	docker-compose build

run:
	docker-compose up

lint: check_format ruff

check_format:
	ruff format --check .
	ruff check --select I .

ruff:
	ruff check . 

format_code:
	ruff check . --fix
	ruff check --select I --fix
	ruff format .
