.PHONY: test


test-env-up:
	@echo "Starting test environment..."
	docker compose -f docker-compose.test.yaml up -d --build

run-tests:
	@echo "Running tests..."
	bash -c 'trap "docker compose -f docker-compose.test.yaml down" EXIT; \
		( cd backend && uv run pytest -q tests/ )'

test-env-down:
	@echo "Cleaning up test environment..."
	docker compose -f docker-compose.test.yaml down -v

test: test-env-up run-tests test-env-down

.PHONY: ty_check
ty_check:
	cd backend && uv run ty check .

.PHONY: mypy_check
mypy_check:
	cd backend && uv run mypy .

.PHONY: coverage 
coverage:
	cd backend && uv run coverage run -m pytest
	cd backend && uv run coverage report
	cd backend && uv run coverage html

