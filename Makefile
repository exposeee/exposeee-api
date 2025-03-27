requirements:
	poetry install

requirements-export:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

requirements-export-dev:
	poetry export --with=dev --without-hashes --format=requirements.txt > requirements.txt

docker-dev: requirements requirements-export-dev \

	docker compose watch