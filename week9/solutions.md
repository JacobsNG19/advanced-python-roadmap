# Packaging, Project Structure & Distribution — Solutions

These solutions correspond to:

```text
Packaging, Project Structure & Distribution - Exercises.md
```

The examples use `uv` for project management and Hatchling as the build backend. Equivalent workflows can be implemented with Poetry, Hatch, or standard `venv` and `pip`.

---

## Exercise 1 — Create a package structure

```text
mini-support/
├── pyproject.toml
├── README.md
├── LICENSE
├── uv.lock
├── src/
│   └── mini_support/
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
└── tests/
    └── test_basic.py
```

Create it with:

```bash
uv init mini-support
cd mini-support
```

Then create the `src/mini_support/` and `tests/` files as needed.

---

## Exercise 2 — Project metadata

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mini-support"
version = "0.1.0"
description = "A small support-ticket CLI."
readme = "README.md"
requires-python = ">=3.12"
authors = [
    { name = "Toussaint Jacobs" },
]
```

The distribution name uses a hyphen, while the import name can use an underscore:

```text
Distribution → mini-support
Import       → mini_support
```

---

## Exercise 3 — Build backend

Use Hatchling:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Build:

```bash
uv build
```

Expected output directory:

```text
dist/
├── mini_support-0.1.0-py3-none-any.whl
└── mini_support-0.1.0.tar.gz
```

Alternatively:

```bash
python -m build
```

---

## Exercise 4 — Runtime dependency

Add a dependency:

```bash
uv add httpx
```

The resulting metadata will contain a runtime dependency similar to:

```toml
[project]
dependencies = [
    "httpx>=0.27",
]
```

Use it in the package:

```python
import httpx


def client_name():
    return httpx.__name__
```

---

## Exercise 5 — Development dependencies

```bash
uv add --dev pytest ruff pyright
```

The project can represent development dependencies as:

```toml
[dependency-groups]
dev = [
    "pytest",
    "ruff",
    "pyright",
]
```

Runtime users do not need these tools to use the package.

---

## Exercise 6 — Virtual environment

With uv:

```bash
uv sync
uv run python -c "import mini_support"
uv run pytest
```

With standard Python:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pytest
```

The `-e` option installs the project in editable mode for development.

---

## Exercise 7 — Console command

`pyproject.toml`:

```toml
[project.scripts]
mini-support = "mini_support.cli:main"
```

`src/mini_support/cli.py`:

```python
def main() -> None:
    print("Mini Support is running.")
```

Run:

```bash
uv sync
uv run mini-support
```

Expected output:

```text
Mini Support is running.
```

---

## Exercise 8 — Module execution

`src/mini_support/__main__.py`:

```python
from .cli import main


if __name__ == "__main__":
    main()
```

Run:

```bash
uv run python -m mini_support
```

Both entry points now call the same `main()` function.

---

## Exercise 9 — Dependency lock

Create or update the lockfile:

```bash
uv lock
```

Install exactly from the lockfile:

```bash
uv sync --locked
```

Commit:

```text
pyproject.toml
uv.lock
```

Do not commit:

```text
.venv/
```

---

## Exercise 10 — Optional feature dependency

```toml
[project.optional-dependencies]
database = [
    "psycopg[binary]>=3.2",
]
```

Install the optional feature:

```bash
pip install mini-support[database]
```

The base installation remains:

```bash
pip install mini-support
```

without the PostgreSQL dependency.

---

## Exercise 11 — Package public API

`src/mini_support/models.py`:

```python
class Ticket:
    def __init__(self, ticket_id, title):
        self.ticket_id = ticket_id
        self.title = title
```

`src/mini_support/__init__.py`:

```python
from .models import Ticket

__all__ = ["Ticket"]
```

Users can now write:

```python
from mini_support import Ticket
```

---

## Exercise 12 — Test the installed artifact

Build:

```bash
uv build
```

Create a clean environment outside the project:

```bash
python -m venv /tmp/mini-support-test
source /tmp/mini-support-test/bin/activate
```

Install the wheel:

```bash
python -m pip install dist/*.whl
```

Verify imports:

```bash
python -c "from mini_support import Ticket; print(Ticket)"
```

Verify the command:

```bash
mini-support
```

This tests the built artifact rather than relying on the source checkout.

---

## Exercise 13 — Package data

Create:

```text
src/mini_support/data/defaults.json
```

Example contents:

```json
{
  "model": "default-model",
  "debug": false
}
```

Read it with `importlib.resources`:

```python
import json
from importlib.resources import files


def load_defaults():
    data_file = files("mini_support").joinpath(
        "data/defaults.json"
    )

    return json.loads(
        data_file.read_text(encoding="utf-8")
    )
```

Build and inspect the wheel to verify the data file is included.

---

## Exercise 14 — Versioning

Initial release:

```toml
version = "0.1.0"
```

Bug fix:

```toml
version = "0.1.1"
```

Backward-compatible feature:

```toml
version = "0.2.0"
```

Build after each version change:

```bash
uv build
```

Do not publish two different artifacts under the same version.

---

## Exercise 15 — TestPyPI workflow

Build:

```bash
uv build
```

Install Twine:

```bash
uv add --dev twine
```

Upload:

```bash
uv run twine upload \
    --repository testpypi \
    dist/*
```

Install from TestPyPI in a clean environment:

```bash
python -m pip install \
    --index-url https://test.pypi.org/simple/ \
    mini-support
```

Use an API token or trusted publishing; do not place credentials in source code.

---

## Exercise 16 — Configuration from environment variables

```python
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    model_name: str
    debug: bool


def load_settings() -> Settings:
    return Settings(
        model_name=os.getenv(
            "MODEL_NAME",
            "default-model",
        ),
        debug=os.getenv(
            "DEBUG",
            "false",
        ).lower() == "true",
    )
```

This reads configuration at runtime while keeping secrets and deployment settings outside the package source.

---

## Exercise 17 — Larger application structure

```text
src/mini_support/
├── domain/
│   └── tickets.py
├── application/
│   └── ticket_service.py
├── infrastructure/
│   ├── file_repository.py
│   └── database.py
├── interfaces/
│   └── repositories.py
├── cli.py
└── config.py
```

Responsibilities:

```text
domain          → ticket concepts and business rules
application     → use cases
infrastructure  → external systems
interfaces      → protocols/contracts
cli.py          → command-line interaction
config.py       → settings
```

---

## Exercise 18 — Protocol boundary

`interfaces/repositories.py`:

```python
from typing import Protocol


class TicketRepository(Protocol):
    def save(self, ticket: dict) -> None:
        ...

    def get_by_id(self, ticket_id: str) -> dict | None:
        ...
```

In-memory implementation:

```python
class InMemoryRepository:
    def __init__(self):
        self._tickets = {}

    def save(self, ticket):
        self._tickets[ticket["id"]] = ticket.copy()

    def get_by_id(self, ticket_id):
        ticket = self._tickets.get(ticket_id)
        return ticket.copy() if ticket else None
```

Application service:

```python
class TicketService:
    def __init__(self, repository: TicketRepository):
        self._repository = repository

    def create(self, ticket: dict) -> dict:
        self._repository.save(ticket)
        return ticket
```

The service depends on the protocol, not the concrete storage class.

---

## Exercise 19 — CI commands

A suitable CI sequence is:

```bash
uv sync --locked
uv run ruff check .
uv run ruff format . --check
uv run pyright
uv run pytest --cov=src --cov-report=term-missing
uv build
```

The locked synchronization step prevents CI from silently resolving a different dependency graph.

---

## Exercise 20 — Final distribution project

Example final metadata:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mini-support"
version = "0.1.0"
description = "A support-ticket application."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "httpx>=0.27,<1.0",
]

[dependency-groups]
dev = [
    "pytest",
    "pytest-cov",
    "ruff",
    "pyright",
]

[project.scripts]
mini-support = "mini_support.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 79
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.pyright]
include = ["src", "tests"]
typeCheckingMode = "standard"
pythonVersion = "3.12"
```

Final workflow:

```bash
uv sync
uv run ruff check .
uv run ruff format . --check
uv run pyright
uv run pytest --cov=src
uv build
```

Test the wheel in a clean environment:

```bash
python -m venv /tmp/mini-support-clean
source /tmp/mini-support-clean/bin/activate
python -m pip install dist/*.whl
python -c "from mini_support import Ticket"
mini-support
```

---

# Review checklist

You should now understand:

- Why `pyproject.toml` is central to modern packaging.
- The roles of `[build-system]`, `[project]`, and `[tool.*]`.
- How virtual environments isolate dependencies.
- How uv manages project dependencies and lockfiles.
- How Hatchling builds distributions.
- How Poetry fits into the packaging ecosystem.
- The difference between runtime and development dependencies.
- Wheels versus source distributions.
- Console scripts and `python -m` execution.
- Why built artifacts must be tested in clean environments.
- How package data is included and loaded.
- How protocols separate application logic from infrastructure.
- How CI verifies a package before distribution.
