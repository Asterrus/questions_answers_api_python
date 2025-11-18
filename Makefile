.PHONY: test

test:
	cd backend && uv run pytest -q

.PHONY: ty_check
ty_check:
	cd backend && uv run ty check .

.PHONY: mypy_check
mypy_check:
	cd backend && uv run mypy .