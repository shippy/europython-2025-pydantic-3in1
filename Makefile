take0:
	uv run uvicorn everything_bagel.app:app --reload

take1:
	uv run uvicorn inheritance_matryoshka.app:app --reload

take2:
	uv run uvicorn overschemed.app:app --reload

take3-generate:
	uv run python src/templating/generate.py

take3: take3-generate
	uv run uvicorn templating.app:app --reload