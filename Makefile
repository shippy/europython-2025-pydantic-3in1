take0:
	uv run uvicorn everything_bagel.app:app --reload --port 8051

take1:
	uv run uvicorn inheritance_matryoshka.app:app --reload --port 8052

take2:
	uv run uvicorn overschemed.app:app --reload --port 8053