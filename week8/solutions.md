# Testing, Quality & Tooling — Solutions

These solutions correspond to:

```text
Testing, Quality & Tooling - Exercises.md
```

Install common tools:

```bash
python -m pip install pytest pytest-cov hypothesis ruff pyright
```

---

## Exercise 1 — Basic behavior test

Application code:

```python
def add(first: int, second: int) -> int:
    return first + second
```

Tests:

```python
from app import add


def test_add_positive_values():
    assert add(2, 3) == 5


def test_add_zero():
    assert add(0, 4) == 4


def test_add_negative_values():
    assert add(-2, -3) == -5
```

Run:

```bash
pytest -q
```

---

## Exercise 2 — Exception testing

Application code:

```python
def divide(first: float, second: float) -> float:
    if second == 0:
        raise ValueError(
            "Cannot divide by zero."
        )

    return first / second
```

Tests:

```python
import pytest

from app import divide


def test_divide_by_zero():
    with pytest.raises(
        ValueError,
        match="Cannot divide by zero",
    ):
        divide(10, 0)
```

For more detail:

```python
def test_exception_value():
    with pytest.raises(ValueError) as error:
        divide(10, 0)

    assert str(error.value) == (
        "Cannot divide by zero."
    )
```

---

## Exercise 3 — Reusable fixture

`tests/conftest.py`:

```python
import pytest


@pytest.fixture
def sample_ticket():
    return {
        "id": "T-001",
        "title": "Cannot log in",
        "priority": "high",
    }
```

Tests:

```python
def test_ticket_id(sample_ticket):
    assert sample_ticket["id"] == "T-001"


def test_ticket_priority(sample_ticket):
    assert sample_ticket["priority"] == "high"
```

Pytest injects the fixture because the test functions request it by name.

---

## Exercise 4 — Fixture cleanup

```python
import pytest


@pytest.fixture
def temporary_resource(tmp_path):
    path = tmp_path / "resource.txt"
    path.write_text("data", encoding="utf-8")

    yield path

    if path.exists():
        path.unlink()
```

Test:

```python
def test_resource(temporary_resource):
    assert temporary_resource.read_text(
        encoding="utf-8"
    ) == "data"
```

Code after `yield` is teardown and runs after the test.

---

## Exercise 5 — Parametrized validation

Application code:

```python
def validate_priority(priority: str) -> str:
    allowed = {"low", "normal", "high"}

    if priority not in allowed:
        raise ValueError("Invalid priority.")

    return priority
```

Tests:

```python
import pytest

from app import validate_priority


@pytest.mark.parametrize(
    "priority",
    ["low", "normal", "high"],
)
def test_valid_priority(priority):
    assert validate_priority(priority) == priority


@pytest.mark.parametrize(
    "priority",
    ["urgent", "", "medium"],
)
def test_invalid_priority(priority):
    with pytest.raises(
        ValueError,
        match="Invalid priority",
    ):
        validate_priority(priority)
```

---

## Exercise 6 — Parametrized boundary cases

```python
def validate_score(score: int) -> int:
    if not 0 <= score <= 100:
        raise ValueError("Score must be 0 through 100.")

    return score
```

```python
import pytest

from app import validate_score


@pytest.mark.parametrize(
    "score",
    [0, 1, 99, 100],
)
def test_valid_score(score):
    assert validate_score(score) == score


@pytest.mark.parametrize(
    "score",
    [-1, 101],
)
def test_invalid_score(score):
    with pytest.raises(ValueError):
        validate_score(score)
```

---

## Exercise 7 — Monkeypatch environment

Application code:

```python
import os


def get_model_name() -> str:
    return os.getenv(
        "MODEL_NAME",
        "default-model",
    )
```

Tests:

```python
def test_custom_model_name(monkeypatch):
    monkeypatch.setenv(
        "MODEL_NAME",
        "test-model",
    )

    assert get_model_name() == "test-model"


def test_default_model_name(monkeypatch):
    monkeypatch.delenv(
        "MODEL_NAME",
        raising=False,
    )

    assert get_model_name() == "default-model"
```

`monkeypatch` automatically restores the environment after each test.

---

## Exercise 8 — Mock an external provider

Application code:

```python
class Assistant:
    def __init__(self, provider):
        self.provider = provider

    def answer(self, question):
        prompt = f"Answer clearly: {question}"
        return self.provider.generate(prompt)
```

Test:

```python
from unittest.mock import Mock


def test_assistant_uses_provider():
    provider = Mock()
    provider.generate.return_value = "Test answer"

    assistant = Assistant(provider)

    result = assistant.answer("What is Python?")

    assert result == "Test answer"
    provider.generate.assert_called_once_with(
        "Answer clearly: What is Python?"
    )
```

---

## Exercise 9 — Mock failures

```python
from unittest.mock import Mock

import pytest


def test_provider_timeout():
    provider = Mock()
    provider.generate.side_effect = TimeoutError(
        "Provider timed out."
    )

    assistant = Assistant(provider)

    with pytest.raises(TimeoutError):
        assistant.answer("Question")


def test_invalid_provider_response():
    provider = Mock()
    provider.generate.return_value = None

    assistant = Assistant(provider)

    with pytest.raises(ValueError):
        assistant.answer("Question")
```

The second test assumes the application validates provider responses. If it does not, add that validation before writing the test.

---

## Exercise 10 — Temporary paths

```python
import json


def test_json_report(tmp_path):
    path = tmp_path / "report.json"
    report = {
        "accuracy": 0.94,
        "samples": 100,
    }

    path.write_text(
        json.dumps(report),
        encoding="utf-8",
    )

    restored = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert restored == report
```

`tmp_path` isolates test files from the project directory.

---

## Exercise 11 — Coverage

Install:

```bash
python -m pip install pytest-cov
```

Run:

```bash
pytest --cov=src --cov-report=term-missing
```

HTML report:

```bash
pytest --cov=src --cov-report=html
```

An uncovered branch example:

```python
def classify(value):
    if value > 0:
        return "positive"

    return "non-positive"
```

If tests only use positive values, coverage should identify the unexecuted branch.

Coverage measures execution, not correctness.

---

## Exercise 12 — Marked tests

`pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: slow tests",
    "integration: integration tests",
]
```

Tests:

```python
import pytest


@pytest.mark.slow
def test_large_operation():
    assert sum(range(100_000)) > 0


@pytest.mark.integration
def test_external_style_workflow():
    assert True
```

Run only slow tests:

```bash
pytest -m slow
```

---

## Exercise 13 — Property-based string test

```python
from hypothesis import given
from hypothesis import strategies as st


def reverse(text: str) -> str:
    return text[::-1]


@given(st.text())
def test_reverse_twice(text):
    assert reverse(reverse(text)) == text
```

Hypothesis generates many strings, including empty and unusual Unicode strings.

---

## Exercise 14 — Property-based sorting test

```python
from hypothesis import given
from hypothesis import strategies as st


def sort_values(values):
    return sorted(values)


@given(st.lists(st.integers()))
def test_sort_properties(values):
    original = list(values)
    result = sort_values(values)

    assert result == sorted(result)
    assert len(result) == len(values)
    assert values == original
```

The copy verifies that the input is not mutated.

---

## Exercise 15 — Property-based ticket test

```python
from hypothesis import given
from hypothesis import strategies as st


PRIORITIES = ["low", "normal", "high"]


ticket_strategy = st.fixed_dictionaries({
    "id": st.text(
        min_size=1,
        max_size=20,
    ),
    "title": st.text(
        min_size=1,
        max_size=100,
    ),
    "priority": st.sampled_from(PRIORITIES),
})


@given(ticket_strategy)
def test_ticket_parser(ticket):
    parsed = parse_ticket(ticket)

    assert isinstance(parsed["id"], str)
    assert isinstance(parsed["title"], str)
    assert parsed["priority"] in PRIORITIES
```

The strategy describes valid input while Hypothesis explores many examples.

---

## Exercise 16 — Logging configuration

```python
import logging
import sys
from logging.handlers import RotatingFileHandler


def configure_logging(path="application.log"):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        path,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)
```

In real applications, protect the configuration from adding duplicate handlers repeatedly.

---

## Exercise 17 — Exception logging

```python
import logging


logger = logging.getLogger(__name__)


def process():
    try:
        raise ValueError("Invalid record.")
    except Exception:
        logger.exception("Processing failed.")
        raise
```

Test:

```python
import pytest


def test_process_reraises():
    with pytest.raises(
        ValueError,
        match="Invalid record",
    ):
        process()
```

`logger.exception()` logs the active traceback. `raise` preserves the original failure.

---

## Exercise 18 — Ruff configuration

`pyproject.toml`:

```toml
[tool.ruff]
line-length = 79
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Run:

```bash
ruff check .
ruff check . --fix
ruff format .
ruff format . --check
```

Use `--check` in CI so formatting differences fail the build without modifying files.

---

## Exercise 19 — Debugging practice

```python
def calculate_total(values):
    total = 0

    for value in values:
        breakpoint()
        total += value

    return total
```

Run the function and inspect:

```text
p values
p value
p total
n
c
```

The debugger lets you inspect state line by line. Remove or disable `breakpoint()` after diagnosing the problem.

---

## Exercise 20 — Final quality pipeline

Example structure:

```text
project/
├── pyproject.toml
├── src/
│   └── app/
│       ├── __init__.py
│       └── tickets.py
└── tests/
    ├── conftest.py
    └── test_tickets.py
```

`pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"

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

Run the complete pipeline:

```bash
ruff check .
ruff format . --check
pyright
pytest --cov=src --cov-report=term-missing
```

A CI job can use the same commands.

---

# Review checklist

You should now understand:

- How pytest discovers and runs tests.
- Fixtures and fixture cleanup.
- Parametrization.
- Mocking and monkeypatching.
- Unit, integration, and end-to-end testing.
- Coverage limitations.
- Hypothesis strategies and properties.
- Logging levels and traceback logging.
- Ruff linting and formatting.
- Breakpoints and traceback-based debugging.
- How to create a repeatable quality pipeline.
