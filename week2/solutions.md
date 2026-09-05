# Iterators, Generators & Context Managers — Complete Exercises

This exercise workbook covers:

- The iterable and iterator protocols.
- Custom iterators with `__iter__` and `__next__`.
- Generators with `yield`.
- Generator expressions.
- `yield from`.
- Lazy pipelines.
- Synchronous context managers.
- `contextlib.contextmanager`.
- `ExitStack`, `closing`, and exception handling.
- Async context managers.

---

## Exercise 1 — Manual iteration

Use `iter()` and `next()` to manually consume this list:

```python
values = [10, 20, 30]
```

### Solution

```python
values = [10, 20, 30]
iterator = iter(values)

assert next(iterator) == 10
assert next(iterator) == 20
assert next(iterator) == 30

try:
    next(iterator)
except StopIteration:
    finished = True
else:
    finished = False

assert finished is True
```

---

## Exercise 2 — Custom countdown iterator

Create a `Countdown` class that counts from a starting number down to zero.

```python
assert list(Countdown(3)) == [3, 2, 1, 0]
```

### Solution

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


assert list(Countdown(3)) == [3, 2, 1, 0]
```

---

## Exercise 3 — Custom range iterator

Create an iterator called `StepRange` that yields numbers from `start` up to, but not including, `stop`, using `step`.

```python
assert list(StepRange(0, 10, 2)) == [0, 2, 4, 6, 8]
```

### Solution

```python
class StepRange:
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


assert list(StepRange(0, 10, 2)) == [0, 2, 4, 6, 8]
assert list(StepRange(5, 0, -2)) == [5, 3, 1]
```

---

## Exercise 4 — Reusable collection versus one-shot iterator

Create a reusable `TicketCollection` whose `__iter__()` returns a fresh iterator each time.

### Solution

```python
class TicketCollection:
    def __init__(self, tickets):
        self._tickets = list(tickets)

    def __iter__(self):
        return iter(self._tickets)

    def __len__(self):
        return len(self._tickets)


collection = TicketCollection([
    "T-001",
    "T-002",
])

assert list(collection) == ["T-001", "T-002"]
assert list(collection) == ["T-001", "T-002"]
assert len(collection) == 2
```

---

## Exercise 5 — Generator: positive values

Create `positive_values(values)` that lazily yields only positive values.

### Solution

```python
def positive_values(values):
    for value in values:
        if value > 0:
            yield value


assert list(positive_values([-2, 0, 3, -1, 5])) == [3, 5]
```

---

## Exercise 6 — Generator: even numbers

Create `even_numbers(limit)` that yields even values from zero through `limit`.

### Solution

```python
def even_numbers(limit: int):
    for number in range(0, limit + 1, 2):
        yield number


assert list(even_numbers(10)) == [0, 2, 4, 6, 8, 10]
```

---

## Exercise 7 — Generator expression

Create a generator expression for the squares of values from `0` to `9`.

### Solution

```python
squares = (
    number * number
    for number in range(10)
)

assert list(squares) == [
    0, 1, 4, 9, 16,
    25, 36, 49, 64, 81,
]
```

---

## Exercise 8 — Lazy file reader

Create `non_empty_lines(path)` that reads a file lazily, strips whitespace, and skips blank lines.

### Solution

```python
def non_empty_lines(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            cleaned = line.strip()

            if cleaned:
                yield cleaned
```

Example test:

```python
from pathlib import Path


path = Path("sample.txt")
path.write_text(
    " First line \n\n Second line \n",
    encoding="utf-8",
)

assert list(non_empty_lines(path)) == [
    "First line",
    "Second line",
]

path.unlink()
```

---

## Exercise 9 — Generator pipeline

Build a lazy pipeline that:

1. Strips strings.
2. Removes empty strings.
3. Converts them to lowercase.

### Solution

```python
def strip_values(values):
    for value in values:
        yield value.strip()


def remove_empty(values):
    for value in values:
        if value:
            yield value


def lowercase(values):
    for value in values:
        yield value.lower()


raw_values = [
    "  Python  ",
    "",
    "  AI  ",
]

pipeline = lowercase(
    remove_empty(
        strip_values(raw_values)
    )
)

assert list(pipeline) == ["python", "ai"]
```

---

## Exercise 10 — `yield from`

Flatten nested batches with `yield from`.

```python
batches = [
    ["T-001", "T-002"],
    ["T-003"],
    ["T-004", "T-005"],
]
```

### Solution

```python
def flatten(batches):
    for batch in batches:
        yield from batch


assert list(flatten(batches)) == [
    "T-001",
    "T-002",
    "T-003",
    "T-004",
    "T-005",
]
```

---

## Exercise 11 — Nested generator delegation

Create `read_sections(sections)` using a helper generator and `yield from`.

### Solution

```python
def read_section(section):
    for value in section:
        yield value


def read_sections(sections):
    for section in sections:
        yield from read_section(section)


sections = [
    ["A", "B"],
    ["C"],
    ["D", "E"],
]

assert list(read_sections(sections)) == [
    "A", "B", "C", "D", "E",
]
```

---

## Exercise 12 — Generator return value

Create a generator that yields numbers and returns a final total.

### Solution

```python
def values_with_total(values):
    total = 0

    for value in values:
        total += value
        yield value

    return total


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

## Exercise 13 — Custom context manager

Create a `Session` context manager that prints setup and cleanup messages and returns itself.

### Solution

```python
class Session:
    def __enter__(self):
        self.opened = True
        print("Session opened.")
        return self

    def send(self, message):
        if not self.opened:
            raise RuntimeError("Session is closed.")

        return f"Sent: {message}"

    def __exit__(self, exc_type, exc_value, traceback):
        self.opened = False
        print("Session closed.")
        return False


with Session() as session:
    assert session.send("Hello") == "Sent: Hello"
```

---

## Exercise 14 — Context manager and exceptions

Create a context manager that prints whether the block succeeded or failed but does not suppress exceptions.

### Solution

```python
class DebugContext:
    def __enter__(self):
        print("Setup.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print("Block succeeded.")
        else:
            print(f"Block failed: {exc_value}")

        print("Cleanup.")
        return False
```

Test failure propagation:

```python
try:
    with DebugContext():
        raise ValueError("Invalid value.")
except ValueError as error:
    assert str(error) == "Invalid value."
```

---

## Exercise 15 — Exception suppression

Create a context manager that suppresses only `ValueError`, while allowing other exceptions to continue.

### Solution

```python
class SuppressValueError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return exc_type is ValueError
```

```python
with SuppressValueError():
    raise ValueError("This is suppressed.")

try:
    with SuppressValueError():
        raise TypeError("This continues.")
except TypeError as error:
    assert str(error) == "This continues."
```

---

## Exercise 16 — Timer class context manager

Create a `Timer` context manager that prints the elapsed time after the block, even when an exception occurs.

### Solution

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


with Timer("Calculation"):
    total = sum(range(100_000))
```

---

## Exercise 17 — `contextmanager` decorator

Rewrite the previous timer using `@contextmanager`.

### Solution

```python
from contextlib import contextmanager
from time import perf_counter


@contextmanager
def timer(label="Block"):
    start = perf_counter()

    try:
        yield
    finally:
        elapsed = perf_counter() - start
        print(
            f"{label}: "
            f"{elapsed:.6f} seconds"
        )


with timer("Calculation"):
    total = sum(range(100_000))
```

---

## Exercise 18 — Context manager with a value

Create a context manager that yields a temporary configuration dictionary and restores the original setting afterward.

### Solution

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


settings = {"debug": False}

with temporary_setting(settings, "debug", True):
    assert settings["debug"] is True

assert settings["debug"] is False
```

---

## Exercise 19 — `contextlib.closing`

Create an object with a `.close()` method but no `__enter__()` or `__exit__()`. Use `closing()` to manage it.

### Solution

```python
from contextlib import closing


class ExternalResource:
    def __init__(self):
        self.closed = False

    def use(self):
        if self.closed:
            raise RuntimeError("Resource is closed.")

        return "resource data"

    def close(self):
        self.closed = True


resource = ExternalResource()

with closing(resource) as item:
    assert item.use() == "resource data"

assert resource.closed is True
```

---

## Exercise 20 — `ExitStack`

Use `ExitStack` to open an arbitrary list of files and read them safely.

### Solution

```python
from contextlib import ExitStack
from pathlib import Path


def read_files(paths):
    with ExitStack() as stack:
        files = [
            stack.enter_context(
                path.open(encoding="utf-8")
            )
            for path in paths
        ]

        return [file.read() for file in files]


first = Path("first.txt")
second = Path("second.txt")

first.write_text("A", encoding="utf-8")
second.write_text("B", encoding="utf-8")

assert read_files([first, second]) == ["A", "B"]

first.unlink()
second.unlink()
```

---

## Exercise 21 — Cleanup callback with `ExitStack`

Register a cleanup function that runs after the context exits.

### Solution

```python
from contextlib import ExitStack


cleaned = []


def cleanup():
    cleaned.append(True)


with ExitStack() as stack:
    stack.callback(cleanup)
    assert cleaned == []

assert cleaned == [True]
```

---

## Exercise 22 — Async context manager

Create an asynchronous connection with `__aenter__()`, `__aexit__()`, and an async query method.

### Solution

```python
import asyncio


class AsyncConnection:
    async def __aenter__(self):
        self.opened = True
        return self

    async def query(self, sql):
        if not self.opened:
            raise RuntimeError("Connection is closed.")

        await asyncio.sleep(0.01)
        return f"Result for: {sql}"

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.opened = False
        return False


async def main():
    async with AsyncConnection() as connection:
        result = await connection.query(
            "SELECT * FROM tickets"
        )

        assert result == (
            "Result for: SELECT * FROM tickets"
        )


asyncio.run(main())
```

---

## Exercise 23 — `asynccontextmanager`

Rewrite the previous async context manager using `@asynccontextmanager`.

### Solution

```python
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def async_session():
    print("Async setup.")

    try:
        yield "ready"
    finally:
        print("Async cleanup.")


async def main():
    async with async_session() as value:
        assert value == "ready"


asyncio.run(main())
```

---

## Exercise 24 — Async generator

Create an async generator that yields three events with a small delay between them.

### Solution

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

## Exercise 25 — Combined streaming pipeline

Build a complete pipeline that:

1. Reads raw ticket dictionaries lazily.
2. Converts them to normalized dictionaries.
3. Filters urgent tickets.
4. Yields only their IDs.
5. Measures the pipeline with a context manager.

### Solution

```python
from contextlib import contextmanager
from time import perf_counter


def ticket_stream(records):
    for record in records:
        yield {
            "id": record["id"],
            "text": record["text"].strip().lower(),
            "priority": record.get(
                "priority",
                "normal",
            ),
        }


def urgent_tickets(tickets):
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
        "text": "Cannot log in",
        "priority": "high",
    },
    {
        "id": "T-002",
        "text": "General question",
        "priority": "normal",
    },
    {
        "id": "T-003",
        "text": "Payment failed",
        "priority": "high",
    },
]

with timer("Ticket pipeline"):
    pipeline = ticket_ids(
        urgent_tickets(
            ticket_stream(records)
        )
    )

    result = list(pipeline)

assert result == ["T-001", "T-003"]
```

---

# Suggested execution order

1. Exercises 1–4: iterator protocol.
2. Exercises 5–12: generators and delegation.
3. Exercises 13–16: class-based context managers.
4. Exercises 17–21: `contextlib` utilities.
5. Exercises 22–24: asynchronous resources and streams.
6. Exercise 25: integrated lazy pipeline.

# Mastery checklist

You should be able to explain:

- Why `iter(obj)` and `next(iterator)` are different operations.
- Why `__next__()` raises `StopIteration`.
- Why a generator is usually one-shot.
- Why `yield` pauses rather than returns permanently.
- When to use `yield from`.
- Why generators help with large data.
- What `__enter__()` returns after `as`.
- Why cleanup belongs in `finally`.
- How `__exit__()` controls exception suppression.
- When to use `@contextmanager` instead of a class.
- Why async resources require `async with`.
- How async generators support streaming.

# Final challenge

Build a small streaming support-ticket processor with:

```text
Ticket source generator
        ↓
Normalization generator
        ↓
Priority filter generator
        ↓
Context-managed timing
        ↓
Result collection
```

Then create an asynchronous version that emits ticket events using an async generator and manages the client using an async context manager.
