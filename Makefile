.PHONY: test

test:
	cd backend && uv run pytest -q

.PHONY: ty_check
ty_check:
	cd backend && uv run ty check .
