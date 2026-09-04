Iterators, generators, and context managers are all **protocols**: Python looks for specific special methods and gives your objects built-in behavior. Iterators produce values one at a time, generators make iterator creation easier, and context managers guarantee setup and cleanup around a `with` block.[[docs.python](https://docs.python.org/3/library/stdtypes.html)]

# 1. The iteration protocol

When you write:

```
for item in collection:
    print(item)
```

Python needs the object to be iterable.

The basic protocol is:

```
__iter__()
__next__()
```

- `__iter__()` returns an iterator.
- `__next__()` returns the next item.
- When no items remain, `__next__()` raises `StopIteration`.

Python’s iterator protocol requires iterators to implement both `__iter__()` and `__next__()`. A container’s `__iter__()` must return an iterator.[[docs.python](https://docs.python.org/3/library/stdtypes.html)]

## Manual iteration

```
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Output:

```
10
20
30
```

Then:

```
next(iterator)
```

raises:

```
StopIteration
```

A `for` loop handles this automatically.

Conceptually:

```
iterator = iter(numbers)

while True:
    try:
        item = next(iterator)
    except StopIteration:
        break

    print(item)
```

---

# 2. Iterable versus iterator

These terms are related but different.

## Iterable

An iterable is an object that can produce an iterator.

Examples:

```
list
tuple
str
dict
set
range
file
generator
```

```
values = [1, 2, 3]

iterator = iter(values)
```

## Iterator

An iterator remembers its current position and produces the next value.

```
iterator = iter(values)

print(next(iterator))
```

A useful test:

```
iterator is iter(iterator)
```

For a real iterator, this is usually:

```
True
```

A container usually produces a new iterator:

```
values = [1, 2, 3]

first_iterator = iter(values)
second_iterator = iter(values)

print(first_iterator is second_iterator)
```

Output:

```
False
```

This means a list can be iterated over repeatedly, while one iterator is normally consumed once.

---

# 3. Creating a custom iterator

Suppose you want a countdown object.

```
class Countdown:
    def __init__(self, start):
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

Use it:

```
countdown = Countdown(3)

for number in countdown:
    print(number)
```

Output:

```
3
2
1
0
```

## How it works

First:

```
iter(countdown)
```

calls:

```
countdown.__iter__()
```

which returns:

```
self
```

Then each loop iteration calls:

```
next(countdown)
```

which runs:

```
countdown.__next__()
```

When the value becomes less than zero:

```
raise StopIteration
```

ends the loop.

---

# 4. Iterator state

The iterator’s state is stored in:

```
self.current
```

After each call:

```
self.current -= 1
```

the object remembers its new position.

```
countdown = Countdown(2)

print(next(countdown))
print(next(countdown))
print(next(countdown))
```

Output:

```
2
1
0
```

The next call raises:

```
StopIteration
```

## One-shot behavior

```
countdown = Countdown(2)

print(list(countdown))
print(list(countdown))
```

Output:

```
[2, 1, 0]
[]
```

The iterator has been exhausted.

---

# 5. Container and iterator design

A container should usually return a fresh iterator rather than return itself.

## Better collection design

```
class TicketCollection:
    def __init__(self, tickets):
        self._tickets = list(tickets)

    def __iter__(self):
        return iter(self._tickets)
```

Use:

```
tickets = TicketCollection([
    "T-001",
    "T-002",
    "T-003",
])

for ticket in tickets:
    print(ticket)

for ticket in tickets:
    print(ticket)
```

Both loops work because each call to:

```
iter(tickets)
```

returns a new iterator.

## A common mistake

```
class BadCollection:
    def __init__(self, items):
        self.items = iter(items)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.items)
```

This object is itself a one-shot iterator. Repeated iteration will not restart.

Use this design only when the object genuinely represents an iterator, not a reusable collection.

---

# 6. Custom iterator with `__getitem__`

Python can sometimes iterate over an object that supports integer indexing.

```
class NumberSequence:
    def __getitem__(self, index):
        if index >= 5:
            raise IndexError

        return index * 10
```

```
sequence = NumberSequence()

for value in sequence:
    print(value)
```

Output:

```
0
10
20
30
40
```

Python begins with index `0` and continues until `IndexError`.

However, prefer defining `__iter__()` explicitly for modern, readable code.

---

# 7. Generators

A generator is a convenient iterator created with `yield`.

```
def count_up_to(limit):
    number = 1

    while number <= limit:
        yield number
        number += 1
```

Use:

```
for number in count_up_to(3):
    print(number)
```

Output:

```
1
2
3
```

A function containing `yield` does not return a normal result immediately. Calling it produces a generator object.

```
generator = count_up_to(3)

print(generator)
```

Output resembles:

```
<generator object count_up_to at 0x...>
```

Execution starts when you call:

```
next(generator)
```

or iterate over it.

---

# 8. `yield` pauses execution

```
def example():
    print("Step one")
    yield 1

    print("Step two")
    yield 2

    print("Step three")
```

```
generator = example()

print(next(generator))
print(next(generator))
```

Output:

```
Step one
1
Step two
2
```

Resume it:

```
try:
    next(generator)
except StopIteration:
    print("Finished")
```

Output:

```
Step three
Finished
```

At each `yield`, the generator:

1. Produces a value.
2. Pauses.
3. Remembers its local variables and position.
4. Resumes when requested.

This is why generators are naturally lazy.

---

# 9. Generator versus normal function

Normal function:

```
def make_numbers(limit):
    numbers = []

    for number in range(limit):
        numbers.append(number)

    return numbers
```

It computes and stores all values.

Generator:

```
def generate_numbers(limit):
    for number in range(limit):
        yield number
```

It computes only when the next value is requested.

## Memory comparison

```
List:
compute all → store all → return collection

Generator:
compute one → yield one → pause → continue later
```

Use generators for:

- Large files.
- Large database results.
- Data preprocessing.
- Streaming API responses.
- Batch pipelines.
- Model evaluation.
- Event streams.
- Potentially infinite sequences.

---

# 10. Generator expressions

A generator expression looks like a list comprehension with parentheses.

```
squares = (
    number * number
    for number in range(5)
)
```

Consume it:

```
print(list(squares))
```

Output:

```
[0, 1, 4, 9, 16]
```

List comprehension:

```
squares = [
    number * number
    for number in range(5)
]
```

Generator expression:

```
squares = (
    number * number
    for number in range(5)
)
```

Use a generator when you want lazy processing:

```
total = sum(
    number * number
    for number in range(1_000_000)
)
```

This avoids creating a million-element list.

---

# 11. Generator pipelines

Generators compose naturally.

```
def read_lines(lines):
    for line in lines:
        yield line.strip()
```

```
def remove_empty(lines):
    for line in lines:
        if line:
            yield line
```

```
def normalize(lines):
    for line in lines:
        yield line.lower()
```

Use:

```
raw_lines = [
    "  Cannot log in  ",
    "",
    "  PAYMENT FAILED ",
]

pipeline = normalize(
    remove_empty(
        read_lines(raw_lines)
    )
)

for line in pipeline:
    print(line)
```

Output:

```
cannot log in
payment failed
```

The pipeline processes each item as it flows through:

```
raw line
   ↓
strip whitespace
   ↓
remove blanks
   ↓
lowercase
   ↓
consumer
```

No unnecessary intermediate lists are created.

---

# 12. Reading large files with generators

```
def error_lines(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            cleaned = line.strip()

            if cleaned and "ERROR" in cleaned:
                yield cleaned
```

Use:

```
for line in error_lines("application.log"):
    print(line)
```

The file is processed line by line.

## Important file-lifetime detail

Correct:

```
def error_lines(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            yield line
```

The generator keeps the `with` block active while it is being consumed.

Incorrect:

```
def error_lines(path):
    with open(path, encoding="utf-8") as file:
        return (
            line
            for line in file
        )
```

The file closes before the returned generator is consumed.

---

# 13. `yield from`

`yield from` delegates to another iterable.

```
def numbers():
    yield from [1, 2, 3]
    yield from [4, 5, 6]
```

```
print(list(numbers()))
```

Output:

```
[1, 2, 3, 4, 5, 6]
```

Without `yield from`:

```
def numbers():
    for number in [1, 2, 3]:
        yield number

    for number in [4, 5, 6]:
        yield number
```

## Nested generator

```
def read_batch(batch):
    for item in batch:
        yield item


def read_batches(batches):
    for batch in batches:
        yield from read_batch(batch)
```

```
batches = [
    ["T-001", "T-002"],
    ["T-003"],
    ["T-004", "T-005"],
]

print(list(read_batches(batches)))
```

Output:

```
['T-001', 'T-002', 'T-003', 'T-004', 'T-005']
```

Use `yield from` when one generator should delegate to another generator or iterable.

---

# 14. Generator return values

A generator can use:

```
return value
```

When it finishes, the value appears inside `StopIteration`.

```
def calculate():
    yield 1
    yield 2
    return "Finished successfully"
```

```
generator = calculate()

print(next(generator))
print(next(generator))

try:
    next(generator)
except StopIteration as error:
    print(error.value)
```

Output:

```
1
2
Finished successfully
```

With `yield from`, the delegated generator’s return value can be captured:

```
def child():
    yield "data"
    return 42
```

```
def parent():
    result = yield from child()
    print(f"Child returned {result}")
```

```
print(list(parent()))
```

Output:

```
Child returned 42
['data']
```

This is advanced generator behavior.

---

# 15. Generator-based coroutines

Historically, Python supported coroutine-like code using generators:

```
@asyncio.coroutine
def old_style():
    yield from something()
```

Modern Python uses native coroutines:

```
async def modern_style():
    await something()
```

The relationship is:

```
Generator:
yield values

Native coroutine:
async def + await asynchronous operations
```

Both pause and resume execution, but they serve different modern purposes.

## Modern code

```
import asyncio


async def fetch_data():
    await asyncio.sleep(1)
    return "Data received"
```

```
async def main():
    result = await fetch_data()
    print(result)


asyncio.run(main())
```

Do not use old generator-based coroutine syntax in new applications. Learn it only so you can understand older code and the historical foundation of `async`/`await`.

## Important distinction

This is a generator:

```
def generate():
    yield 1
```

This is a native coroutine:

```
async def fetch():
    await asyncio.sleep(1)
```

A generator produces values.

A coroutine represents an asynchronous operation.

---

# 16. Context managers

A context manager controls a resource during a block:

```
with resource:
    use(resource)
```

Typical resources:

- Files.
- Database transactions.
- Locks.
- Temporary directories.
- Network sessions.
- Model sessions.
- Configuration overrides.

A context manager implements:

```
__enter__()
__exit__()
```

Example:

```
class SimpleContext:
    def __enter__(self):
        print("Entering context.")
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        print("Exiting context.")
        return False
```

Use it:

```
with SimpleContext():
    print("Inside block.")
```

Output:

```
Entering context.
Inside block.
Exiting context.
```

---

# 17. Context manager with `as`

```
class Session:
    def __enter__(self):
        print("Session opened.")
        return self

    def send(self, message):
        return f"Sent: {message}"

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        print("Session closed.")
        return False
```

Use:

```
with Session() as session:
    print(session.send("Hello"))
```

Output:

```
Session opened.
Sent: Hello
Session closed.
```

The expression after `as` receives the return value of:

```
__enter__()
```

Since `__enter__()` returns `self`, the variable `session` refers to the context-manager object.

---

# 18. Context managers and exceptions

```
class DebugContext:
    def __enter__(self):
        print("Setup.")
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        if exc_type is None:
            print("No exception.")

        else:
            print(
                f"Exception: {exc_type.__name__}"
            )
            print(f"Message: {exc_value}")

        print("Cleanup.")
        return False
```

Use:

```
with DebugContext():
    raise ValueError("Invalid input.")
```

Output:

```
Setup.
Exception: ValueError
Message: Invalid input.
Cleanup.
```

The exception continues because:

```
return False
```

or:

```
return None
```

means:

```
Do not suppress the exception.
```

---

# 19. Suppressing exceptions

Returning `True` from `__exit__()` suppresses the exception.

```
class IgnoreValueErrors:
    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return exc_type is ValueError
```

```
with IgnoreValueErrors():
    raise ValueError("Ignored.")
```

The program continues after the block.

Use this only when suppression is deliberately part of the API. Never silently suppress every exception:

```
def __exit__(self, exc_type, exc_value, traceback):
    return True
```

That hides bugs and operational failures.

---

# 20. `contextlib.contextmanager`

Writing `__enter__()` and `__exit__()` manually is not always necessary.

Use:

```
from contextlib import contextmanager
```

```
@contextmanager
def simple_context():
    print("Setup.")

    try:
        yield
    finally:
        print("Cleanup.")
```

Use it:

```
with simple_context():
    print("Inside block.")
```

Output:

```
Setup.
Inside block.
Cleanup.
```

The `contextmanager` decorator converts a generator function into a context manager. The code before `yield` is setup; the code after `yield` is cleanup.[[docs.python](https://docs.python.org/3/library/contextlib.html)]

---

# 21. Context manager with a value

```
from contextlib import contextmanager


@contextmanager
def prepared_value():
    value = {
        "status": "ready",
    }

    try:
        yield value
    finally:
        print("Value cleanup.")
```

Use:

```
with prepared_value() as data:
    print(data)
```

Output:

```
{'status': 'ready'}
Value cleanup.
```

The value after `yield` becomes the value after `as`.

---

# 22. Exception handling with `contextmanager`

```
from contextlib import contextmanager


@contextmanager
def log_errors():
    try:
        yield

    except Exception as error:
        print(f"Error recorded: {error}")
        raise

    finally:
        print("Cleanup completed.")
```

Use:

```
with log_errors():
    raise RuntimeError("Operation failed.")
```

Output:

```
Error recorded: Operation failed.
Cleanup completed.
```

The `raise` is important because it allows the original exception to continue.

If you omit it:

```
except Exception as error:
    print(error)
```

the exception is suppressed.

---

# 23. Timing context manager

```
from contextlib import contextmanager
from time import perf_counter


@contextmanager
def timer(label: str):
    start = perf_counter()

    try:
        yield

    finally:
        elapsed = perf_counter() - start

        print(
            f"{label}: "
            f"{elapsed:.6f} seconds"
        )
```

Use:

```
with timer("Processing"):
    total = sum(range(1_000_000))
```

Possible output:

```
Processing: 0.018421 seconds
```

This is useful for measuring:

- API requests.
- Retrieval.
- Model inference.
- Database queries.
- Data preprocessing.
- Agent tools.

---

# 24. Temporary configuration context manager

```
from contextlib import contextmanager


@contextmanager
def temporary_setting(
    settings: dict,
    key: str,
    value,
):
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

Use:

```
settings = {
    "debug": False,
}

with temporary_setting(
    settings,
    "debug",
    True,
):
    print(settings)
```

Output:

```
{'debug': True}
```

After the block:

```
print(settings)
```

Output:

```
{'debug': False}
```

This is useful for tests and temporary model configuration.

---

# 25. Async context managers

Synchronous resources use:

```
with
```

Asynchronous resources use:

```
async with
```

They implement:

```
__aenter__()
__aexit__()
```

Example:

```
import asyncio


class AsyncSession:
    async def __aenter__(self):
        print("Opening async session.")
        return self

    async def fetch(self, url):
        await asyncio.sleep(1)
        return f"Fetched {url}"

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        print("Closing async session.")
```

Use:

```
async def main():
    async with AsyncSession() as session:
        result = await session.fetch(
            "https://example.com"
        )

        print(result)


asyncio.run(main())
```

The `contextlib` module also provides async context-manager utilities such as `asynccontextmanager`.[[docs.python](https://docs.python.org/3/library/contextlib.html)]

---

# 26. `asynccontextmanager`

```
from contextlib import asynccontextmanager
import asyncio
```

```
@asynccontextmanager
async def async_session():
    print("Async setup.")

    try:
        yield "Async resource"

    finally:
        print("Async cleanup.")
```

Use:

```
async def main():
    async with async_session() as resource:
        print(resource)

    print("Finished.")
```

```
asyncio.run(main())
```

Output:

```
Async setup.
Async resource
Async cleanup.
Finished.
```

Use `asynccontextmanager` when setup or cleanup needs:

```
await
```

---

# 27. `contextlib.closing`

Some objects have:

```
close()
```

but do not implement `__enter__()` and `__exit__()`.

Adapt them with:

```
from contextlib import closing
```

```
class ExternalResource:
    def use(self):
        return "Resource used."

    def close(self):
        print("Resource closed.")
```

Use:

```
resource = ExternalResource()

with closing(resource) as item:
    print(item.use())
```

Output:

```
Resource used.
Resource closed.
```

Conceptually:

```
try:
    use(resource)
finally:
    resource.close()
```

---

# 28. `ExitStack`

Use `ExitStack` when resources are dynamic.

```
from contextlib import ExitStack
```

```
filenames = [
    "part1.txt",
    "part2.txt",
    "part3.txt",
]
```

```
with ExitStack() as stack:
    files = [
        stack.enter_context(
            open(filename, encoding="utf-8")
        )
        for filename in filenames
    ]

    contents = [
        file.read()
        for file in files
    ]
```

All files are closed when the stack exits.

`ExitStack` is useful when:

- The number of resources is not known beforehand.
- Resources are conditionally opened.
- You need to register cleanup callbacks.
- Multiple context managers must be combined dynamically.

Cleanup happens in reverse order of registration.[[docs.python](https://docs.python.org/3/library/contextlib.html)]

---

# 29. Combining generators and context managers

These concepts work well together.

```
from contextlib import contextmanager


@contextmanager
def open_lines(path):
    file = open(path, encoding="utf-8")

    try:
        yield (
            line.strip()
            for line in file
            if line.strip()
        )

    finally:
        file.close()
```

Use:

```
with open_lines("tickets.txt") as lines:
    for line in lines:
        print(line)
```

The context manager controls the file lifecycle.

The generator expression processes lines lazily.

This pattern is useful for:

```
resource management + streaming processing
```

---

# 30. Realistic AI pipeline

```
from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
```

```
@dataclass
class Ticket:
    ticket_id: str
    text: str
```

Lazy ticket generator:

```
def generate_tickets(
    records: list[dict[str, str]],
):
    for record in records:
        yield Ticket(
            ticket_id=record["id"],
            text=record["text"].strip(),
        )
```

Filter:

```
def important_tickets(
    tickets,
):
    for ticket in tickets:
        if "urgent" in ticket.text.lower():
            yield ticket
```

Timing context:

```
@contextmanager
def measure(label: str):
    start = perf_counter()

    try:
        yield

    finally:
        elapsed = perf_counter() - start

        print(
            f"{label}: "
            f"{elapsed:.6f} seconds"
        )
```

Use the pipeline:

```
records = [
    {
        "id": "T-001",
        "text": "Urgent login failure",
    },
    {
        "id": "T-002",
        "text": "General question",
    },
    {
        "id": "T-003",
        "text": "Urgent payment failure",
    },
]
```

```
with measure("Ticket pipeline"):
    tickets = generate_tickets(records)
    important = important_tickets(tickets)

    for ticket in important:
        print(ticket)
```

Output:

```
Ticket(ticket_id='T-001', text='Urgent login failure')
Ticket(ticket_id='T-003', text='Urgent payment failure')
Ticket pipeline: 0.000...
```

This combines:

```
dataclass      → structured ticket
generator      → lazy input processing
generator      → lazy filtering
contextmanager → timing and cleanup
```

---

# 31. Common mistakes

## Forgetting `yield`

Incorrect:

```
def numbers():
    return [1, 2, 3]
```

This returns a list, not a generator.

Correct:

```
def numbers():
    yield 1
    yield 2
    yield 3
```

---

## Expecting a generator to restart

```
generator = (x for x in range(3))

list(generator)
list(generator)
```

The second result is empty.

Create a new generator or store a list if repeated access is required.

---

## Returning an iterator instead of a fresh iterator

For reusable containers:

```
class Collection:
    def __iter__(self):
        return iter(self._items)
```

Do not make the collection itself a consumed iterator unless that is intentional.

---

## Forgetting `StopIteration`

A custom `__next__()` must signal completion:

```
raise StopIteration
```

Do not return `None` to signal the end. `None` may be a legitimate value.

---

## Forgetting `return self` in `__enter__`

Incorrect:

```
def __enter__(self):
    self.connect()
```

Then:

```
with Connection() as connection:
    connection.query()
```

`connection` becomes `None`.

Correct:

```
def __enter__(self):
    self.connect()
    return self
```

---

## Cleanup outside `finally`

Incorrect:

```
@contextmanager
def resource():
    setup()
    yield
    cleanup()
```

Correct:

```
@contextmanager
def resource():
    setup()

    try:
        yield

    finally:
        cleanup()
```

---

## Suppressing unexpected exceptions

Avoid:

```
def __exit__(self, exc_type, exc_value, traceback):
    return True
```

Usually return:

```
False
```

to allow errors to propagate.

---

## Blocking inside async context managers

Avoid:

```
async def __aenter__(self):
    time.sleep(5)
```

Use asynchronous operations:

```
async def __aenter__(self):
    await asyncio.sleep(5)
```

or move blocking work to a thread.

# 32. Practice exercises

## Exercise 1: Custom iterator

Create:

```
class Countdown:
    ...
```

It should count from a starting number down to zero.

Implement:

```
__iter__
__next__
```

## Exercise 2: Generator

Create:

```
def read_positive_numbers(values):
    ...
```

It should yield only positive numbers lazily.

## Exercise 3: `yield from`

Create a generator that flattens:

```
[
    [1, 2],
    [3],
    [4, 5],
]
```

## Exercise 4: Context manager

Create a `Timer` class with:

```
__enter__
__exit__
```

It should print the elapsed time.

## Exercise 5: `contextmanager`

Create:

```
@contextmanager
def temporary_value():
    ...
```

It should yield a temporary dictionary and print cleanup afterward.

## Exercise 6: Async context manager

Create:

```
AsyncConnection
```

with:

```
__aenter__
__aexit__
```

Use `async with`.

# 33. Exercise answers

## Exercise 1 answer

```
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

```
for number in Countdown(3):
    print(number)
```

## Exercise 2 answer

```
def read_positive_numbers(values):
    for value in values:
        if value > 0:
            yield value
```

```
values = [-2, 0, 3, -1, 5]

print(list(read_positive_numbers(values)))
```

Output:

```
[3, 5]
```

## Exercise 3 answer

```
def flatten(groups):
    for group in groups:
        yield from group
```

```
print(list(flatten([
    [1, 2],
    [3],
    [4, 5],
])))
```

Output:

```
[1, 2, 3, 4, 5]
```

## Exercise 4 answer

```
from time import perf_counter


class Timer:
    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        elapsed = perf_counter() - self.start

        print(
            f"Elapsed: {elapsed:.6f} seconds"
        )

        return False
```

```
with Timer():
    total = sum(range(1_000_000))
```

## Exercise 5 answer

```
from contextlib import contextmanager
```

```
@contextmanager
def temporary_value():
    value = {
        "status": "temporary",
    }

    try:
        yield value

    finally:
        print("Temporary value cleaned up.")
```

```
with temporary_value() as value:
    print(value)
```

## Exercise 6 answer

```
import asyncio


class AsyncConnection:
    async def __aenter__(self):
        print("Connection opened.")
        return self

    async def query(self, sql):
        await asyncio.sleep(0.1)
        return f"Result for: {sql}"

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        print("Connection closed.")
        return False
```

```
async def main():
    async with AsyncConnection() as connection:
        result = await connection.query(
            "SELECT * FROM tickets"
        )

        print(result)


asyncio.run(main())
```

# 34. Final mental model

## Custom iterator

```
class Iterator:
    def __iter__(self):
        return self

    def __next__(self):
        if finished:
            raise StopIteration

        return next_value
```

Use when you need full control over iteration state.

## Generator

```
def generator():
    yield value
```

Use for simpler, lazy iteration.

## Generator expression

```
(value for value in values)
```

Use for compact lazy transformations.

## `yield from`

```
yield from other_iterable
```

Use to delegate iteration.

## Synchronous context manager

```
class Resource:
    def __enter__(self):
        ...

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        ...
```

Use with:

```
with Resource():
    ...
```

## Generator-based context manager

```
@contextmanager
def resource():
    setup()

    try:
        yield value
    finally:
        cleanup()
```

## Asynchronous context manager

```
class AsyncResource:
    async def __aenter__(self):
        ...

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        ...
```

Use with:

```
async with AsyncResource():
    ...
```

The core relationships are:

```
Iterator       → controls next values
Generator      → easier way to create an iterator
yield          → produce one value and pause
yield from     → delegate to another iterator
Context manager → guarantees setup and cleanup
async/await    → modern asynchronous pause/resume model
```

For your AI-engineering projects:

```
Large ticket files     → generators
Data pipelines         → generator composition
Experiment streams     → itertools + generators
Model resource setup   → context managers
Database transactions  → context managers
Async model clients    → async context managers
Streaming model output → async generators
```

Learn custom iterators to understand the protocol, but use generators for most normal lazy iteration. Learn class-based context managers to understand the lifecycle, but use `contextlib.contextmanager` when setup and cleanup are simple. Native `async`/`await` is the modern coroutine model; generator-based coroutines are mainly important for understanding older Python code and the conceptual foundation of pausing and resuming execution.[[docs.python](https://docs.python.org/3/library/stdtypes.html)][[docs.python](https://docs.python.org/3/library/contextlib.html)]
