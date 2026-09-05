# Testing, Quality & Tooling — Exercises

## Instructions

Solve each question independently. Choose your own implementation. The requirements describe expected behavior without prescribing how you must implement it.

Use a professional workflow:

```bash
pytest
ruff check .
ruff format --check .
pyright
```

---

## Exercise 1 — Basic behavior test

Create tests for a function that adds two numbers.

Test:

- Positive values.
- Zero.
- Negative values.

---

## Exercise 2 — Exception testing

Create tests for a division function that rejects division by zero.

Verify both:

- The exception type.
- The exception message.

---

## Exercise 3 — Reusable fixture

Create a reusable test setup for a sample ticket containing:

```text
id
 title
priority
```

Use it in at least two tests.

---

## Exercise 4 — Fixture cleanup

Create a test resource that creates a temporary file before a test and removes or closes the resource afterward.

Verify that cleanup happens even when the test body raises an exception.

---

## Exercise 5 — Parametrized validation

Create one parametrized test covering valid and invalid ticket priorities.

Valid values:

```text
low
normal
high
```

Invalid values should raise an exception.

---

## Exercise 6 — Parametrized boundary cases

Test a function that accepts an integer from `0` through `100`.

Cover:

```text
0
1
99
100
-1
101
```

---

## Exercise 7 — Monkeypatch environment

Create a configuration function that reads `MODEL_NAME` from the environment and uses a default when it is absent.

Test both situations without changing the real environment permanently.

---

## Exercise 8 — Mock an external provider

Create a service that calls an external model provider.

Test the service without making a real network or model call.

Verify that the provider was called with the expected prompt.

---

## Exercise 9 — Mock failures

Test how the service behaves when the external provider:

- Raises a timeout.
- Returns an invalid response.

---

## Exercise 10 — Temporary paths

Create a test that writes a JSON report to a temporary directory and reads it back.

The test must not create files in the project root.

---

## Exercise 11 — Coverage

Configure pytest coverage for the source directory.

Run tests with a terminal report showing missing lines.

Create one deliberately untested branch and confirm that coverage reports it.

---

## Exercise 12 — Marked tests

Create and register these marks:

```text
slow
integration
```

Write one test for each and run only the slow tests.

---

## Exercise 13 — Property-based string test

Using Hypothesis, test that reversing a string twice returns the original string.

---

## Exercise 14 — Property-based sorting test

Using Hypothesis, test properties of a sorting function:

- Output is sorted.
- Output length equals input length.
- Input is not changed.

---

## Exercise 15 — Property-based ticket test

Generate ticket dictionaries with valid priorities and test that your parser always returns a valid ticket structure.

---

## Exercise 16 — Logging configuration

Configure logging so that:

- Console output shows `INFO` and above.
- A file receives `DEBUG` and above.
- Both outputs contain timestamp, level, logger name, and message.

---

## Exercise 17 — Exception logging

Create a function that logs an exception with its traceback and then re-raises it.

Test that the original exception is still raised.

---

## Exercise 18 — Ruff configuration

Create a `pyproject.toml` configuration for Ruff that:

- Sets a line length.
- Enables common lint rules.
- Enables import sorting.
- Configures formatting.

Run linting and formatting checks.

---

## Exercise 19 — Debugging practice

Create a deliberately failing function.

Debug it using:

```python
breakpoint()
```

Inspect at least two variables and step through at least three lines.

---

## Exercise 20 — Final quality pipeline

Create a small package with:

- Source code.
- Unit tests.
- A fixture.
- Parametrized tests.
- A mocked external dependency.
- A Hypothesis property test.
- Logging.
- Ruff configuration.
- Static type checking.
- Coverage reporting.

Run the full quality pipeline successfully.

# Practice rules

- Tests must verify behavior, not merely execute lines.
- Keep unit tests independent.
- Mock external services at the boundary.
- Do not log secrets.
- Do not hide failures with broad exception handling.
- Keep formatting and linting automated.
