# Iterators, Generators & Context Managers — Solutions

These solutions correspond to:

```text
Iterators, Generators & Context Managers - Exercises.md
```

---

## Exercise 1 — Consume a sequence

```python
values = [10, 20, 30]
iterator = iter(values)

while True:
    try:
        print(next(iterator))
    except StopIteration:
        break
```

`iter()` obtains an iterator, while `next()` requests the next value. `StopIteration` signals completion.

---

## Exercise 2 — Countdown

```python
class Countdown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration

        value = self.current
        self.current -= 1
        return value
```

---

## Exercise 3 — Step sequence

```python
class StepSequence:
    def __init__(self, start, stop, step=1):
        if step == 0:
            raise ValueError("step cannot be zero.")

        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.step > 0 and self.current >= self.stop:
            raise StopIteration

        if self.step < 0 and self.current <= self.stop:
            raise StopIteration

        value = self.current
        self.current += self.step
        return value
```

---

## Exercise 4 — Reusable collection

```python
class TicketCollection:
    def __init__(self, ticket_ids):
        self._ticket_ids = list(ticket_ids)

    def __iter__(self):
        return iter(self._ticket_ids)

    def __len__(self):
        return len(self._ticket_ids)

    def __getitem__(self, index):
        return self._ticket_ids[index]
```

The collection returns a fresh iterator each time, so repeated iteration works.

---

## Exercise 5 — Positive values

```python
def positive_values(values):
    for value in values:
        if value > 0:
            yield value
```

---

## Exercise 6 — Even numbers

```python
def even_numbers(limit):
    for number in range(0, limit + 1, 2):
        yield number
```

---

## Exercise 7 — Squares

```python
def squares():
    return (
        number * number
        for number in range(10)
    )
```

This returns a lazy generator expression.

---

## Exercise 8 — Non-empty file lines

```python
def non_empty_lines(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            cleaned = line.strip()

            if cleaned:
                yield cleaned
```

The file remains open while the generator is being consumed because the `with` block is inside the generator function.

---

## Exercise 9 — Text processing pipeline

```python
def process_text(values):
    stripped = (
        value.strip()
        for value in values
    )

    non_empty = (
        value
        for value in stripped
        if value
    )

    return (
        value.lower()
        for value in non_empty
    )
```

All stages are lazy until the caller consumes the result.

---

## Exercise 10 — Flatten batches

```python
def flatten(batches):
    for batch in batches:
        yield from batch
```

`yield from` delegates value production to each nested batch.

---

## Exercise 11 — Stream with a final total

```python
def values_with_total(values):
    total = 0

    for value in values:
        total += value
        yield value

    return total
```

The return value is stored in the final `StopIteration.value`.

Example:

```python
generator = values_with_total([1, 2, 3])

assert next(generator) == 1
assert next(generator) == 2
assert next(generator) == 3

try:
    next(generator)
except StopIteration as error:
    assert error.value == 6
```

---

## Exercise 12 — Resource session

```python
class Session:
    def __enter__(self):
        self.active = True
        return self

    def send(self, message):
        if not self.active:
            raise RuntimeError("Session is inactive.")

        return f"Sent: {message}"

    def __exit__(self, exc_type, exc_value, traceback):
        self.active = False
        return False
```

---

## Exercise 13 — Cleanup after success and failure

```python
class CleanupResource:
    def __init__(self):
        self.cleaned = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleaned = True
        return False
```

Success:

```python
resource = CleanupResource()

with resource:
    pass

assert resource.cleaned is True
```

Failure:

```python
resource = CleanupResource()

try:
    with resource:
        raise ValueError("Failure")
except ValueError:
    pass

assert resource.cleaned is True
```

---

## Exercise 14 — Suppress one exception type

```python
class SuppressValueError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return exc_type is ValueError
```

`__exit__()` returns `True` only for `ValueError`; other exceptions continue normally.

---

## Exercise 15 — Timer resource

```python
from time import perf_counter


class Timer:
    def __init__(self, label="Block"):
        self.label = label

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = perf_counter() - self.start
        print(
            f"{self.label}: "
            f"{elapsed:.6f} seconds"
        )
        return False
```

The cleanup code runs from `__exit__()` regardless of whether the block succeeds or raises.

---

## Exercise 16 — Temporary setting

```python
from contextlib import contextmanager


@contextmanager
def temporary_setting(settings, key, value):
    existed = key in settings
    old_value = settings.get(key)

    settings[key] = value

    try:
        yield settings
    finally:
        if existed:
            settings[key] = old_value
        else:
            settings.pop(key, None)
```

Test an existing key:

```python
settings = {"debug": False}

with temporary_setting(settings, "debug", True):
    assert settings["debug"] is True

assert settings["debug"] is False
```

Test a missing key:

```python
settings = {}

with temporary_setting(settings, "debug", True):
    assert settings["debug"] is True

assert "debug" not in settings
```

---

## Exercise 17 — Managed text file

```python
class ManagedFile:
    def __init__(self, path, mode="r"):
        self.path = path
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(
            self.path,
            self.mode,
            encoding="utf-8",
        )
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file is not None:
            self.file.close()

        return False
```

In ordinary application code, prefer Python’s built-in `open()` context manager. This exercise demonstrates the protocol.

---

## Exercise 18 — Dynamic file reading

```python
from contextlib import ExitStack


def read_files(paths):
    with ExitStack() as stack:
        files = [
            stack.enter_context(
                path.open(encoding="utf-8")
            )
            for path in paths
        ]

        return [file.read() for file in files]
```

`ExitStack` closes all registered resources when the block exits.

---

## Exercise 19 — Async session

```python
import asyncio


class AsyncSession:
    async def __aenter__(self):
        self.active = True
        return self

    async def fetch(self, resource):
        if not self.active:
            raise RuntimeError("Session is inactive.")

        await asyncio.sleep(0.01)
        return f"Fetched: {resource}"

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.active = False
        return False
```

Use:

```python
async def main():
    async with AsyncSession() as session:
        result = await session.fetch("resource")
        assert result == "Fetched: resource"


asyncio.run(main())
```

---

## Exercise 20 — Async event stream

```python
import asyncio


async def event_stream():
    for event in [
        "ticket.created",
        "ticket.classified",
        "ticket.closed",
    ]:
        await asyncio.sleep(0.01)
        yield event


async def main():
    events = []

    async for event in event_stream():
        events.append(event)

    assert events == [
        "ticket.created",
        "ticket.classified",
        "ticket.closed",
    ]


asyncio.run(main())
```

---

## Exercise 21 — Final streaming pipeline

```python
from contextlib import contextmanager
from time import perf_counter


def normalize_tickets(records):
    for record in records:
        yield {
            "id": record["id"],
            "text": record["text"].strip().lower(),
            "priority": record.get(
                "priority",
                "normal",
            ),
        }


def high_priority(tickets):
    for ticket in tickets:
        if ticket["priority"] == "high":
            yield ticket


def ticket_ids(tickets):
    for ticket in tickets:
        yield ticket["id"]


@contextmanager
def timer(label):
    start = perf_counter()

    try:
        yield
    finally:
        elapsed = perf_counter() - start
        print(
            f"{label}: "
            f"{elapsed:.6f} seconds"
        )


records = [
    {
        "id": "T-001",
        "text": " Urgent login failure ",
        "priority": "high",
    },
    {
        "id": "T-002",
        "text": "General question",
        "priority": "normal",
    },
    {
        "id": "T-003",
        "text": " Urgent payment failure ",
        "priority": "high",
    },
]

with timer("Ticket pipeline"):
    result = list(
        ticket_ids(
            high_priority(
                normalize_tickets(records)
            )
        )
    )

assert result == ["T-001", "T-003"]
```

The pipeline remains lazy until `list()` consumes it.

---

# Review checklist

You should now understand:

- The difference between an iterable and an iterator.
- Why `__iter__()` and `__next__()` are needed.
- Why `StopIteration` ends iteration.
- Why generators are lazy and usually one-shot.
- How `yield from` delegates production.
- How generator pipelines avoid unnecessary intermediate lists.
- How `__enter__()` and `__exit__()` implement `with`.
- How `__exit__()` receives exception information.
- How returning `True` suppresses an exception.
- Why cleanup belongs in `finally`.
- How `contextmanager` simplifies context-manager creation.
- Why async resources use `async with`.
- How async generators support streaming.
