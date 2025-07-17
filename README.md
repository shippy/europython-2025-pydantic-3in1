## EuroPython 2025: Pydantic, Everywhere, All at Once

This is a **companion repo** for [my EuroPython 2025 talk](https://ep2025.europython.eu/session/pydantic-everywhere-all-at-once). [You can find the slides on my personal website.](https://simon.podhajsky.net/presentations/europython_2025_pydantic)

> Ever tried using “one data model to rule them all” and ended up with a tangle of constraints, endpoints, and SQL tables? You’re not alone! In this talk, we’ll explore the lofty dream of unifying your Pydantic models across constrained LLM generation, FastAPI inputs/outputs, and SQLModel ORM definitions. But, is it possible to keep a single source of truth without driving yourself (and your teammates) nuts? Or should you split them up and keep everyone happy? We’ll tackle practical examples, including the joys (and pains) (mostly pains) of juggling Pydantic v1 vs. v2. You’ll leave with a clear framework for deciding how best to structure your models and a road map for staying sane when you want Pydantic for **all the things.**


## Setup

1. Install [uv](https://docs.astral.sh/uv/)
2. Run `uv sync`.
3. Run `make takeN` (`take0`...`take2`) to run the corresponding take's FastAPI server.

## Layout

Everything lives in the `src` directory. There is a subdirectory for each take.

### Take 0: The Everything Bagel

A single model with liberal use of `SkipJSONSchema` to simulate private fields.

### Take 1: The Inheritance Matryoshka

A set of models inheriting from a base model. Public fields go in the base model, private fields go in the child model(s).

### Take 2: Overschemed

A single domain model `dataclass(slots=True)`; an independent interface Pydantic model for each boundary. Best but wordy.