Professional Python quality practice is a loop:

```text
Write code → test behavior → inspect failures → lint/format → type-check → debug → automate in CI
```

`pytest` verifies behavior, Hypothesis explores many inputs, Ruff improves consistency, logging explains runtime behavior, and a debugger helps inspect execution interactively.

# 1. Advanced pytest

Install:

```bash
python -m pip install pytest
```

Run tests:

```bash
pytest
```

Useful commands:

```bash
pytest -v                 # Verbose output
pytest -q                 # Compact output
pytest tests/             # Specific directory
pytest tests/test_user.py # Specific file
pytest -k ticket          # Tests matching "ticket"
pytest -x                # Stop after first failure
pytest --tb=short         # Short tracebacks
pytest --collect-only    # Show discovered tests
```

A pytest test is normally a function whose name starts with:

```text
test_
```

Example:

```python
def add(first: int, second: int) -> int:
    return first + second
```

```python
def test_add():
    assert add(2, 3) == 5
```

Run:

```bash
pytest
```

The central pytest pattern is:

```text
Arrange → Act → Assert
```

```python
def test_add():
    # Arrange
    first = 2
    second = 3

    # Act
    result = add(first, second)

    # Assert
    assert result == 5
```

# 2. Testing exceptions

Use:

```python
import pytest
```

```python
def divide(first: float, second: float) -> float:
    if second == 0:
        raise ValueError(
            "Cannot divide by zero."
        )

    return first / second
```

Test:

```python
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

Check the exception message:

```python
def test_divide_by_zero_message():
    with pytest.raises(
        ValueError,
        match="Cannot divide by zero",
    ):
        divide(10, 0)
```

You can inspect the exception:

```python
def test_exception_details():
    with pytest.raises(ValueError) as error:
        divide(10, 0)

    assert str(error.value) == (
        "Cannot divide by zero."
    )
```

# 3. Fixtures

A fixture prepares reusable test data or resources.

```python
import pytest
```

```python
@pytest.fixture
def sample_ticket():
    return {
        "id": "T-001",
        "title": "Cannot log in",
        "priority": "high",
    }
```

Use it by naming it as a test argument:

```python
def test_ticket_id(sample_ticket):
    assert sample_ticket["id"] == "T-001"
```

Pytest discovers fixtures by their function names and injects them into tests that request them. [docs.pytest](https://docs.pytest.org/en/stable/how-to/fixtures.html)

## Fixture setup and teardown

Use `yield`:

```python
@pytest.fixture
def temporary_file(tmp_path):
    path = tmp_path / "ticket.txt"

    path.write_text(
        "Cannot log in",
        encoding="utf-8",
    )

    yield path

    # Cleanup after the test
    if path.exists():
        path.unlink()
```

Test:

```python
def test_temporary_file(temporary_file):
    assert temporary_file.read_text(
        encoding="utf-8"
    ) == "Cannot log in"
```

Everything before `yield` is setup.

Everything after `yield` is teardown.

Pytest’s built-in `tmp_path` fixture creates a temporary directory unique to the test invocation, which is safer than writing test files into your project directory.

## Fixture scopes

```python
@pytest.fixture(scope="function")
def resource():
    ...
```

Common scopes:

| Scope | Created |
|---|---|
| `function` | Once per test; default |
| `class` | Once per test class |
| `module` | Once per test file |
| `package` | Once per package |
| `session` | Once for the whole test run |

Example:

```python
@pytest.fixture(scope="session")
def expensive_model():
    return load_model()
```

Use broader scopes carefully. Shared state can make tests interact with one another.

## Fixture dependencies

```python
@pytest.fixture
def database():
    db = create_database()

    yield db

    db.close()
```

```python
@pytest.fixture
def ticket_repository(database):
    return TicketRepository(database)
```

```python
def test_save_ticket(ticket_repository):
    ...
```

Fixtures can depend on other fixtures. Pytest resolves the dependency graph automatically.

# 4. `conftest.py`

Put shared fixtures in:

```text
tests/conftest.py
```

Example:

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

Tests in that directory and its subdirectories can use:

```python
def test_ticket(sample_ticket):
    ...
```

without importing the fixture manually.

A typical structure:

```text
project/
├── src/
│   └── trustdesk/
│       └── tickets.py
└── tests/
    ├── conftest.py
    ├── test_tickets.py
    └── test_api.py
```

Keep `conftest.py` focused. Do not hide too much setup there, or tests become difficult to understand.

# 5. Parametrization

Parametrization runs one test with multiple data sets.

```python
import pytest
```

```python
@pytest.mark.parametrize(
    "first, second, expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (10, 5, 15),
    ],
)
def test_add(first, second, expected):
    assert add(first, second) == expected
```

Pytest creates a separate test case for each parameter set. This is useful for testing boundary values and many equivalent scenarios. [docs.pytest](https://docs.pytest.org/en/stable/how-to/parametrize.html)

## Parametrize with IDs

```python
@pytest.mark.parametrize(
    "value, expected",
    [
        pytest.param(
            "",
            False,
            id="empty",
        ),
        pytest.param(
            "Python",
            True,
            id="valid-text",
        ),
    ],
)
def test_is_valid_text(value, expected):
    assert is_valid_text(value) is expected
```

Failure output becomes easier to understand:

```text
test_is_valid_text[empty]
test_is_valid_text[valid-text]
```

## Parametrizing fixtures

```python
@pytest.fixture(
    params=["low", "normal", "high"]
)
def priority(request):
    return request.param
```

```python
def test_priority_is_string(priority):
    assert isinstance(priority, str)
```

The test runs once for each fixture parameter. Pytest supports parametrized fixtures for running dependent tests against several configurations. [docs.pytest](https://docs.pytest.org/en/stable/how-to/fixtures.html)

# 6. Marks

Marks classify or control tests.

```python
import pytest
```

```python
@pytest.mark.slow
def test_large_model_evaluation():
    ...
```

Run only slow tests:

```bash
pytest -m slow
```

Register custom marks in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: tests that take significant time",
    "integration: tests requiring external systems",
]
```

Other useful marks:

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    ...
```

```python
@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Unix-only test",
)
def test_unix_behavior():
    ...
```

```python
@pytest.mark.xfail(reason="Known bug")
def test_known_failure():
    ...
```

Do not use `xfail` to hide ordinary failures permanently. Track the issue and remove the mark when fixed.

# 7. Mocking and dependency replacement

Mocking replaces a dependency during a test.

Suppose:

```python
def fetch_user(user_id):
    return call_external_api(
        f"/users/{user_id}"
    )
```

Testing this directly would require a real external API.

Use `unittest.mock`:

```python
from unittest.mock import patch
```

```python
def test_fetch_user():
    with patch(
        "module_name.call_external_api"
    ) as mock_api:
        mock_api.return_value = {
            "id": "U-001",
            "name": "Toussaint",
        }

        result = fetch_user("U-001")

    assert result["name"] == "Toussaint"

    mock_api.assert_called_once_with(
        "/users/U-001"
    )
```

## Patch where the name is used

This is a critical rule.

If `service.py` contains:

```python
from client import call_api
```

then patch:

```python
patch("service.call_api")
```

not necessarily:

```python
patch("client.call_api")
```

You patch the reference used by the code under test.

# 8. `monkeypatch`

Pytest provides the `monkeypatch` fixture for safely changing:

- Attributes.
- Dictionary values.
- Environment variables.
- `sys.path`.
- Functions.
- Module-level configuration.

The changes are automatically undone after the test. [docs.pytest](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)

## Patch an environment variable

```python
import os


def get_model_name():
    return os.getenv(
        "MODEL_NAME",
        "default-model",
    )
```

```python
def test_model_name(monkeypatch):
    monkeypatch.setenv(
        "MODEL_NAME",
        "test-model",
    )

    assert get_model_name() == "test-model"
```

## Delete an environment variable

```python
def test_default_model(monkeypatch):
    monkeypatch.delenv(
        "MODEL_NAME",
        raising=False,
    )

    assert get_model_name() == "default-model"
```

## Patch an attribute

```python
def test_external_call(monkeypatch):
    def fake_call(url):
        return {"status": "ok"}

    monkeypatch.setattr(
        "module_name.call_external_api",
        fake_call,
    )
```

Use `monkeypatch` for straightforward replacement. Use `unittest.mock` when you need call assertions, side effects, call counts, or detailed mock behavior.

# 9. Mock return values and side effects

```python
from unittest.mock import Mock
```

```python
mock_client = Mock()

mock_client.get.return_value = {
    "status": 200,
    "data": "ok",
}

response = mock_client.get("/health")

assert response["status"] == 200
mock_client.get.assert_called_once_with(
    "/health"
)
```

Raise an exception:

```python
mock_client.get.side_effect = TimeoutError(
    "Request timed out."
)
```

Return different values:

```python
mock_client.get.side_effect = [
    TimeoutError("Temporary failure"),
    {"status": 200},
]
```

The first call raises, and the second returns the dictionary.

## Mocking an AI provider

```python
class Assistant:
    def __init__(self, provider):
        self.provider = provider

    def answer(self, question):
        return self.provider.generate(question)
```

```python
def test_assistant():
    provider = Mock()

    provider.generate.return_value = (
        "Test response"
    )

    assistant = Assistant(provider)

    result = assistant.answer(
        "What is Python?"
    )

    assert result == "Test response"

    provider.generate.assert_called_once_with(
        "What is Python?"
    )
```

This test does not call a real model, consume tokens, or depend on network access.

# 10. Integration versus unit tests

## Unit test

Tests one component in isolation:

```python
def test_classifier():
    result = classifier.classify(
        "Payment failed"
    )

    assert result == "billing"
```

External dependencies are replaced.

## Integration test

Tests several real components together:

```python
def test_ticket_service_with_database():
    ...
```

It may use:

- A temporary database.
- A local model.
- A test API.
- Containers.
- A test file system.

## End-to-end test

Tests a complete user workflow:

```text
CLI request → service → database → response
```

A useful testing pyramid:

```text
Many fast unit tests
        ↓
Fewer integration tests
        ↓
A small number of end-to-end tests
```

# 11. Coverage

Install:

```bash
python -m pip install pytest-cov
```

Run:

```bash
pytest --cov=src --cov-report=term-missing
```

Generate HTML:

```bash
pytest \
    --cov=src \
    --cov-report=html
```

Coverage shows which lines or branches were executed.

It does not prove correctness.

This code may have 100% line coverage but still be wrong:

```python
def discount(price):
    return price * 2
```

Coverage answers:

```text
Did the tests execute this line?
```

It does not answer:

```text
Did the tests verify the correct behavior?
```

Use coverage to find untested areas, not as the only quality metric.

# 12. Property-based testing with Hypothesis

Example-based test:

```python
def test_reverse():
    assert reverse("abc") == "cba"
```

Property-based test:

```text
For many generated strings, reversing twice returns the original.
```

Install:

```bash
python -m pip install hypothesis
```

```python
from hypothesis import given
from hypothesis import strategies as st
```

```python
def reverse(text: str) -> str:
    return text[::-1]
```

```python
@given(st.text())
def test_reverse_twice(text):
    assert reverse(reverse(text)) == text
```

Hypothesis generates many values, including unusual Unicode, empty strings, and edge cases you may not manually think of. Its documentation describes property-based tests as tests that state properties for generated inputs rather than relying only on hand-written examples. [hypothesis.readthedocs](https://hypothesis.readthedocs.io/)

## Example: sorting property

```python
@given(st.lists(st.integers()))
def test_sorted_output(values):
    result = sorted(values)

    assert result == sorted(result)
    assert len(result) == len(values)
```

## Example: round-trip property

```python
import json


@given(st.dictionaries(
    st.text(min_size=1),
    st.integers(),
))
def test_json_round_trip(data):
    encoded = json.dumps(data)
    decoded = json.loads(encoded)

    assert decoded == data
```

## Strategies

Common strategies:

```python
st.integers()
st.floats()
st.text()
st.booleans()
st.binary()
st.lists(strategy)
st.sets(strategy)
st.dictionaries(keys, values)
st.tuples(...)
st.one_of(...)
st.just(value)
```

Constrain values:

```python
st.integers(
    min_value=0,
    max_value=100,
)
```

```python
st.text(
    min_size=1,
    max_size=100,
)
```

## Composite strategies

```python
from hypothesis import strategies as st
```

```python
@st.composite
def tickets(draw):
    return {
        "id": draw(
            st.text(
                min_size=1,
                max_size=10,
            )
        ),
        "priority": draw(
            st.sampled_from([
                "low",
                "normal",
                "high",
            ])
        ),
    }
```

Use it:

```python
@given(tickets())
def test_ticket_has_required_fields(ticket):
    assert "id" in ticket
    assert "priority" in ticket
```

## Hypothesis shrinking

When Hypothesis finds a failure, it tries to reduce the input to a smaller failing example.

Instead of showing a huge complicated string, it may find:

```text
empty string
```

or:

```text
integer 0
```

This makes bugs easier to reproduce.

## Good properties

For a classifier:

```text
Output category belongs to allowed categories.
Confidence is between 0 and 1.
```

For a parser:

```text
Valid input never crashes.
Round-trip serialization preserves data.
```

For a queue:

```text
FIFO order is preserved.
```

For a budget:

```text
Remaining budget never becomes negative.
```

For a cache:

```text
Cached and uncached results are equal.
```

# 13. Logging best practices

Use module loggers:

```python
import logging


logger = logging.getLogger(__name__)
```

Do not configure the root logger in every module.

Configure logging once at application startup:

```python
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    ),
)
```

Use levels correctly:

```python
logger.debug("Detailed internal state.")
logger.info("Application started.")
logger.warning("Using fallback configuration.")
logger.error("Operation failed.")
logger.critical("Application cannot continue.")
```

Use lazy formatting:

```python
logger.info(
    "Ticket %s created",
    ticket_id,
)
```

rather than:

```python
logger.info(
    f"Ticket {ticket_id} created"
)
```

Log exceptions with traceback:

```python
try:
    process_ticket(ticket)

except Exception:
    logger.exception(
        "Ticket processing failed."
    )
    raise
```

Never log:

- Passwords.
- API keys.
- Tokens.
- Payment data.
- Full private conversations.
- Unnecessary personal information.

For AI systems, log safe metadata:

```python
logger.info(
    "Classification complete "
    "ticket_id=%s model=%s "
    "category=%s latency_ms=%.2f",
    ticket_id,
    model_name,
    category,
    latency_ms,
)
```

# 14. Ruff: linting and formatting

Ruff is a fast Python linter and formatter written in Rust. Its formatter is designed as a drop-in replacement for Black, and its linter can replace several common tools depending on configuration. [docs.astral](https://docs.astral.sh/ruff/faq/)

Install:

```bash
python -m pip install ruff
```

Check lint errors:

```bash
ruff check .
```

Automatically fix safe errors:

```bash
ruff check . --fix
```

Format files:

```bash
ruff format .
```

Check formatting without changing files:

```bash
ruff format . --check
```

## Basic configuration

In `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",
    "F",
    "I",
    "B",
    "UP",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Common rule groups:

| Code | Meaning |
|---|---|
| `E` | pycodestyle errors |
| `F` | Pyflakes errors |
| `I` | Import sorting |
| `B` | Bugbear-style likely bugs |
| `UP` | Python modernization |
| `S` | Security-related checks |
| `SIM` | Simplification suggestions |
| `C4` | Comprehension improvements |

Start with:

```toml
select = ["E", "F", "I", "B", "UP"]
```

Then add more rules deliberately.

## Ruff workflow

```bash
ruff check . --fix
ruff format .
pytest
pyright
```

Ruff’s linter and formatter can be used independently, so you can adopt one without automatically adopting the other. [docs.astral](https://docs.astral.sh/ruff/faq/)

# 15. Debugging techniques

## Read the traceback from the bottom up

Example:

```text
Traceback (most recent call last):
  File "service.py", line 20, in create_ticket
    return repository.save(ticket)
  File "repository.py", line 12, in save
    self.db.execute(query)
sqlite3.OperationalError: database is locked
```

Start at the bottom:

```text
sqlite3.OperationalError: database is locked
```

Then inspect the call chain upward.

Ask:

```text
What exception happened?
Where did it happen?
What called that line?
What values caused it?
```

## `breakpoint()`

Insert:

```python
def classify_ticket(ticket):
    breakpoint()

    return classifier.classify(ticket)
```

Run the program and use the debugger prompt:

```text
p ticket
p ticket["title"]
n
s
c
```

Common debugger commands:

| Command | Meaning |
|---|---|
| `p expression` | Print expression |
| `pp expression` | Pretty-print expression |
| `n` | Next line |
| `s` | Step into function |
| `r` | Run until current function returns |
| `c` | Continue |
| `l` | Show source |
| `w` | Show stack |
| `q` | Quit debugger |

## Conditional breakpoint

```python
if ticket["priority"] == "high":
    breakpoint()
```

This avoids stopping on every iteration.

## Logging versus debugger

Use logging for:

```text
behavior over time
production diagnosis
distributed systems
background workers
reproducible operational events
```

Use a debugger for:

```text
local step-by-step investigation
unexpected state
control-flow understanding
examining variables
```

# 16. Assertions

Assertions check developer assumptions:

```python
def process_score(score: float):
    assert 0 <= score <= 1
    return score
```

Assertions are useful for internal invariants:

```python
assert result.category in ALLOWED_CATEGORIES
```

Do not use assertions as primary user-input validation because Python can disable them with optimization flags:

```bash
python -O app.py
```

For external data, use explicit exceptions:

```python
if not 0 <= score <= 1:
    raise ValueError(
        "Score must be between 0 and 1."
    )
```

# 17. Professional project configuration

A compact `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
markers = [
    "slow: slow tests",
    "integration: integration tests",
]

[tool.ruff]
line-length = 79
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.ruff.format]
quote-style = "double"

[tool.pyright]
include = ["src", "tests"]
typeCheckingMode = "standard"
pythonVersion = "3.12"
```

Or configure mypy:

```toml
[tool.mypy]
python_version = "3.12"
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
```

Useful development commands:

```bash
ruff check .
ruff format --check .
pytest
pytest --cov=src --cov-report=term-missing
pyright
```

# 18. CI quality pipeline

A basic CI sequence:

```text
1. Install dependencies.
2. Run Ruff linting.
3. Check formatting.
4. Run static type checker.
5. Run tests.
6. Generate coverage.
```

Example:

```yaml
- name: Lint
  run: ruff check .

- name: Format check
  run: ruff format . --check

- name: Type check
  run: pyright

- name: Tests
  run: pytest --cov=src --cov-report=term-missing
```

A pull request should fail when:

- Lint errors exist.
- Formatting differs.
- Type checking fails.
- Tests fail.
- Coverage rules fail, if configured.

# 19. Professional test design

Good tests are:

- Deterministic.
- Independent.
- Fast where possible.
- Focused.
- Readable.
- Repeatable.
- Explicit about dependencies.
- Free from unnecessary external services.

Avoid:

```python
def test_everything():
    ...
```

Prefer focused tests:

```python
def test_ticket_priority_is_valid():
    ...


def test_ticket_cannot_have_empty_title():
    ...


def test_ticket_repository_saves_ticket():
    ...
```

Use realistic boundaries:

```text
empty input
zero
negative values
very large values
missing keys
unknown categories
timeouts
duplicate data
Unicode text
network failure
```

# 20. Complete example

Application code:

```python
from dataclasses import dataclass
from typing import Literal


Priority = Literal[
    "low",
    "normal",
    "high",
]
```

```python
@dataclass
class Ticket:
    title: str
    priority: Priority

    def __post_init__(self):
        self.title = self.title.strip()

        if not self.title:
            raise ValueError(
                "Title cannot be empty."
            )
```

```python
def create_ticket(
    title: str,
    priority: Priority = "normal",
) -> Ticket:
    if priority not in {
        "low",
        "normal",
        "high",
    }:
        raise ValueError(
            "Invalid priority."
        )

    return Ticket(
        title=title,
        priority=priority,
    )
```

Pytest tests:

```python
import pytest
```

```python
@pytest.mark.parametrize(
    "priority",
    ["low", "normal", "high"],
)
def test_valid_priorities(priority):
    ticket = create_ticket(
        "Cannot log in",
        priority,
    )

    assert ticket.priority == priority
```

```python
def test_empty_title_is_rejected():
    with pytest.raises(
        ValueError,
        match="Title cannot be empty",
    ):
        create_ticket("   ")
```

Hypothesis test:

```python
from hypothesis import given
from hypothesis import strategies as st
```

```python
@given(
    st.text(
        min_size=1,
        max_size=100,
    ).filter(lambda text: bool(text.strip()))
)
def test_ticket_title_is_trimmed(title):
    ticket = create_ticket(title)

    assert ticket.title == title.strip()
    assert ticket.title
```

Run quality tools:

```bash
ruff check .
ruff format .
pyright
pytest --cov=src --cov-report=term-missing
```

# 21. Final mental model

```text
pytest
  → Does the code behave correctly?

fixtures
  → How do tests receive reusable setup?

parametrization
  → How do I test many cases without duplication?

mocking
  → How do I isolate external dependencies?

Hypothesis
  → What happens across many automatically generated inputs?

logging
  → What happened while the program was running?

Ruff
  → Is the code consistent, modern, and suspicious-pattern-free?

debugger
  → What are the exact values and control-flow state right now?

coverage
  → Which code has not been executed by tests?
```

For your projects, use this command sequence:

```bash
ruff check . --fix
ruff format .
pyright
pytest --cov=src --cov-report=term-missing
```

The most important professional habits are:

```text
Test public behavior, not implementation details.
Use fixtures for reusable setup and teardown.
Use parametrization for boundaries and repeated cases.
Mock external APIs and model providers.
Use Hypothesis for invariants and edge cases.
Log safe operational metadata, never secrets.
Use Ruff automatically.
Debug with tracebacks, logging, and breakpoints.
Run the entire quality pipeline in CI.
```

For TrustDesk or Burvex, a good quality stack is:

```text
pytest       → unit and integration tests
Hypothesis   → property-based tests for parsers and domain rules
Ruff         → linting and formatting
Pyright      → static typing
logging      → runtime diagnostics
coverage     → untested-code discovery
CI           → automatic enforcement
```

The goal is not merely to have tools installed. The goal is to create a feedback system that catches errors early, makes failures understandable, and keeps the codebase safe to change. [docs.pytest](https://docs.pytest.org/en/stable/how-to/parametrize.html)
