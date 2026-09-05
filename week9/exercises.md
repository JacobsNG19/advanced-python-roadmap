# Packaging, Project Structure & Distribution — Exercises

## Instructions

Solve each question independently. Choose your own implementation and packaging workflow. The requirements describe the desired project behavior without prescribing every design decision.

You may use `uv`, Hatch, Poetry, or standard `venv` and `pip` where appropriate.

---

## Exercise 1 — Create a package structure

Create a project named `mini_support` using a `src/` layout.

It must contain:

```text
pyproject.toml
README.md
src/mini_support/__init__.py
src/mini_support/cli.py
tests/
```

---

## Exercise 2 — Project metadata

Write project metadata containing:

```text
name
version
description
README reference
supported Python version
author
```

Use a modern `pyproject.toml` configuration.

---

## Exercise 3 — Build backend

Configure a build backend and make the project buildable.

The project must produce both:

```text
wheel distribution
source distribution
```

---

## Exercise 4 — Runtime dependency

Add a runtime dependency used by the package.

Install the dependency through your selected project manager and verify that it appears in the project metadata.

---

## Exercise 5 — Development dependencies

Add development dependencies for:

```text
pytest
Ruff
one static type checker
```

Keep development dependencies separate from runtime dependencies.

---

## Exercise 6 — Virtual environment

Create an isolated project environment.

Verify that:

- The project can be installed into the environment.
- The package can be imported.
- The test command uses the project environment.

---

## Exercise 7 — Console command

Expose a command named:

```text
mini-support
```

The command must call a `main()` function in your package.

Verify it works after installation.

---

## Exercise 8 — Module execution

Make the package executable with:

```bash
python -m mini_support
```

The module execution path and console-command path should call the same application entry point.

---

## Exercise 9 — Dependency lock

Generate a dependency lockfile using your selected tool.

Recreate the environment from the lockfile and verify that the application still works.

---

## Exercise 10 — Optional feature dependency

Create an optional dependency group for a database integration.

The base package must remain installable without the database dependency.

---

## Exercise 11 — Package public API

Expose one public class from the package root so users can write:

```python
from mini_support import Ticket
```

Do not require users to import from a deeply nested internal path.

---

## Exercise 12 — Test the installed artifact

Build the package, create a clean environment outside the source checkout, install the wheel, and verify:

- The package imports.
- The public class is available.
- The console command works.

---

## Exercise 13 — Package data

Include a non-Python file, such as a default configuration file, in the installed package.

Verify that installed code can locate and read the file.

---

## Exercise 14 — Versioning

Create a versioning workflow.

Release these changes as:

```text
0.1.0 → initial release
0.1.1 → bug fix
0.2.0 → compatible feature
```

Do not reuse an already-published version.

---

## Exercise 15 — TestPyPI workflow

Build the distributions and upload them to TestPyPI.

Install the package from TestPyPI into a clean environment.

Do not place credentials in source code.

---

## Exercise 16 — Configuration from environment variables

Create a typed settings object that reads:

```text
MODEL_NAME
DEBUG
```

Use safe defaults when values are absent.

---

## Exercise 17 — Larger application structure

Organize a package into:

```text
domain
application
infrastructure
interfaces
cli
```

Give each area one clear responsibility.

---

## Exercise 18 — Protocol boundary

Create a repository interface and two implementations:

```text
in-memory repository
file-backed repository
```

The application service must depend on the interface rather than either concrete implementation.

---

## Exercise 19 — CI commands

Create a CI-style command sequence that:

1. Installs dependencies from the lockfile.
2. Checks formatting.
3. Runs linting.
4. Runs static type checking.
5. Runs tests.
6. Builds the package.

---

## Exercise 20 — Final distribution project

Build a complete installable package with:

- `src/` layout.
- Metadata.
- Runtime dependency.
- Development dependency group.
- Lockfile.
- Public API.
- Console command.
- Tests.
- Package data.
- Wheel and source distribution.
- Clean-environment installation test.

# Practice rules

- Do not commit `.venv`.
- Do not publish secrets.
- Test built artifacts, not only source imports.
- Keep runtime and development dependencies separate.
- Keep internal modules separate from the public API.
