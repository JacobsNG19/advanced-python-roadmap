# Advanced Functions & Functional Tools — Solutions

This file contains the solutions to the questions in:

```text
Advanced Functions & Functional Tools - Exercises.md
```

---

## Exercise 1 — Configurable price calculation

```python
def make_price_calculator(percent: float):
    if not 0 <= percent <= 100:
        raise ValueError(
            "Discount must be between 0 and 100."
        )

    multiplier = 1 - percent / 100

    def calculate(price: float) -> float:
        if price < 0:
            raise ValueError(
                "Price cannot be negative."
            )

        return price * multiplier

    return calculate
```

The returned function remembers `multiplier` from the enclosing call.

---

## Exercise 2 — Independent counters

```python
def make_counter(start: int = 0):
    count = start

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    return increment
```

`nonlocal` allows the nested function to update the variable from the enclosing function.

---

## Exercise 3 — Text formatter factory

```python
def make_formatter(prefix: str, suffix: str):
    def format_text(value: str) -> str:
        return f"{prefix}{value}{suffix}"

    return format_text
```

The nested function captures `prefix` and `suffix`.

---

## Exercise 4 — Operation runner

```python
from collections.abc import Callable


def run_operation(
    operation: Callable[[int, int], int],
    first: int,
    second: int,
) -> int:
    return operation(first, second)
```

The function receives another function as a value and invokes it.

---

## Exercise 5 — Transform a sequence

```python
from collections.abc import Callable, Iterable
from typing import TypeVar


T = TypeVar("T")
R = TypeVar("R")


def transform_all(
    values: Iterable[T],
    transform: Callable[[T], R],
) -> list[R]:
    return [
        transform(value)
        for value in values
    ]
```

The two type variables preserve the relationship between input and output values.

---

## Exercise 6 — Flexible statistics

```python
def statistics(*numbers: int | float):
    if not numbers:
        raise ValueError(
            "At least one number is required."
        )

    total = sum(numbers)

    return {
        "count": len(numbers),
        "minimum": min(numbers),
        "maximum": max(numbers),
        "total": total,
        "average": total / len(numbers),
    }
```

`numbers` is collected as a tuple.

---

## Exercise 7 — Profile builder

```python
def build_profile(**attributes):
    return dict(attributes)
```

`attributes` is already a new dictionary created for the call. Calling `dict()` makes the copying intention explicit.

---

## Exercise 8 — Argument forwarding

```python
def call_with_arguments(function, positional, keywords):
    return function(*positional, **keywords)
```

`*positional` expands the sequence into positional arguments. `**keywords` expands the dictionary into keyword arguments.

---

## Exercise 9 — Logging wrapper

```python
from functools import wraps


def with_logging(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"Calling {function.__name__}")
        result = function(*args, **kwargs)
        print(f"Finished {function.__name__}")
        return result

    return wrapper
```

`wraps()` preserves the original function metadata.

---

## Exercise 10 — Positive first argument

```python
from functools import wraps


def require_positive(function):
    @wraps(function)
    def wrapper(value, *args, **kwargs):
        if value <= 0:
            raise ValueError(
                "Value must be positive."
            )

        return function(
            value,
            *args,
            **kwargs,
        )

    return wrapper
```

This solution assumes the first argument is the value that must be checked.

---

## Exercise 11 — Configurable repetition

```python
from functools import wraps


def repeat(times: int):
    if times < 1:
        raise ValueError(
            "times must be at least 1."
        )

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = None

            for _ in range(times):
                result = function(*args, **kwargs)

            return result

        return wrapper

    return decorator
```

The outer function receives decorator configuration. The middle function receives the target function. The inner function replaces it.

---

## Exercise 12 — Retry temporary failures

```python
from functools import wraps


def retry(attempts: int):
    if attempts < 1:
        raise ValueError(
            "attempts must be at least 1."
        )

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            last_error = None

            for _ in range(attempts):
                try:
                    return function(*args, **kwargs)
                except ConnectionError as error:
                    last_error = error

            raise last_error

        return wrapper

    return decorator
```

Only `ConnectionError` is retried. Other exceptions propagate immediately.

---

## Exercise 13 — Class registration

```python
PLUGIN_REGISTRY = {}


def register_plugin(name: str):
    def decorator(cls):
        if name in PLUGIN_REGISTRY:
            raise ValueError(
                f"Plugin already registered: {name}"
            )

        PLUGIN_REGISTRY[name] = cls
        return cls

    return decorator
```

Example:

```python
@register_plugin("search")
class SearchPlugin:
    def run(self, text):
        return f"Searching: {text}"
```

Retrieve it:

```python
plugin = PLUGIN_REGISTRY["search"]()
assert plugin.run("Python") == "Searching: Python"
```

---

## Exercise 14 — Specialized notification functions

```python
from functools import partial


def send_notification(
    channel: str,
    recipient: str,
    message: str,
) -> str:
    return f"{channel} to {recipient}: {message}"


send_email = partial(
    send_notification,
    "email",
)

send_sms = partial(
    send_notification,
    "sms",
)
```

`partial()` pre-fills the first argument and returns a new callable.

---

## Exercise 15 — Cached Fibonacci

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(number: int) -> int:
    if number < 0:
        raise ValueError(
            "number cannot be negative."
        )

    if number < 2:
        return number

    return (
        fibonacci(number - 1)
        + fibonacci(number - 2)
    )
```

Inspect and clear the cache:

```python
print(fibonacci.cache_info())
fibonacci.cache_clear()
```

The recursive function becomes efficient because previous results are reused.

---

## Exercise 16 — Type-specific serialization

```python
from functools import singledispatch


@singledispatch
def serialize(value):
    raise TypeError(
        f"Unsupported type: {type(value).__name__}"
    )


@serialize.register
def _(value: str):
    return {
        "type": "string",
        "value": value,
    }


@serialize.register
def _(value: int):
    return {
        "type": "integer",
        "value": value,
    }


@serialize.register
def _(value: list):
    return {
        "type": "list",
        "items": [serialize(item) for item in value],
    }
```

`singledispatch` chooses the implementation based on the first argument type.

---

## Exercise 17 — Lazy positive values

```python
def positive_values(values):
    for value in values:
        if value > 0:
            yield value
```

The function returns a generator and does not process all values until consumed.

---

## Exercise 18 — Lazy text pipeline

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

Each stage produces values lazily.

---

## Exercise 19 — Flatten batches and limit results

```python
from itertools import chain, islice


def first_items(batches, limit):
    flattened = chain.from_iterable(batches)
    return list(islice(flattened, limit))
```

`chain.from_iterable()` flattens lazily. `islice()` stops after the requested limit.

---

## Exercise 20 — Group sorted records

```python
from collections import defaultdict
from itertools import groupby


def group_by_category(records):
    grouped = defaultdict(list)

    for category, items in groupby(
        records,
        key=lambda item: item["category"],
    ):
        grouped[category].extend(items)

    return dict(grouped)
```

This assumes records with the same category are consecutive, as specified. If the input is not sorted, sort it by category before using `groupby()`.

---

## Exercise 21 — Experiment combinations

```python
from itertools import product


def experiment_grid(models, temperatures):
    return [
        {
            "model": model,
            "temperature": temperature,
        }
        for model, temperature in product(
            models,
            temperatures,
        )
    ]
```

`product()` creates the Cartesian product of the input sequences.

---

## Exercise 22 — Running totals

```python
from itertools import accumulate


def running_totals(expenses):
    return list(accumulate(expenses))
```

---

## Exercise 23 — Lazy ticket pipeline

```python
from itertools import islice


def high_priority_ids(tickets, limit):
    high_priority = (
        ticket
        for ticket in tickets
        if ticket["priority"] == "high"
    )

    identifiers = (
        ticket["id"]
        for ticket in high_priority
    )

    return list(islice(identifiers, limit))
```

The generator expressions avoid creating intermediate lists.

---

## Exercise 24 — Final mini-project

```python
from collections import Counter
from functools import partial, wraps


def make_id_generator(prefix="T"):
    number = 0

    def next_id():
        nonlocal number
        number += 1
        return f"{prefix}-{number:03d}"

    return next_id


def create_ticket(
    title,
    category="general",
    priority="normal",
):
    return {
        "title": title,
        "category": category,
        "priority": priority,
    }


def ticket_stream(records):
    for record in records:
        yield {
            "id": record["id"],
            "title": record["title"].strip(),
            "category": record.get(
                "category",
                "general",
            ),
            "priority": record.get(
                "priority",
                "normal",
            ),
        }


def high_priority(tickets):
    for ticket in tickets:
        if ticket["priority"] == "high":
            yield ticket


def log_call(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"Calling {function.__name__}")
        result = function(*args, **kwargs)
        print(f"Finished {function.__name__}")
        return result

    return wrapper


@log_call
def count_categories(tickets):
    return Counter(
        ticket["category"]
        for ticket in tickets
    )


next_ticket_id = make_id_generator()

create_urgent_ticket = partial(
    create_ticket,
    priority="high",
)


first_id = next_ticket_id()
second_id = next_ticket_id()

assert first_id == "T-001"
assert second_id == "T-002"

records = [
    {
        "id": first_id,
        "title": "Cannot log in",
        "category": "account_access",
        "priority": "high",
    },
    {
        "id": second_id,
        "title": "Invoice is incorrect",
        "category": "billing",
        "priority": "normal",
    },
]

urgent = list(
    high_priority(
        ticket_stream(records)
    )
)

counts = count_categories(urgent)

new_ticket = create_urgent_ticket(
    "Production outage",
    category="technical",
)

assert counts["account_access"] == 1
assert new_ticket["priority"] == "high"
```

---

# Review checklist

Before considering the module complete, make sure you understand:

- How closures retain values.
- Why `nonlocal` is needed for changing closure state.
- How late binding occurs in loops.
- How `*args` and `**kwargs` collect and forward arguments.
- How decorators replace functions.
- Why `functools.wraps` matters.
- Why parameterized decorators need an additional function layer.
- When `partial()` is clearer than a wrapper.
- When caching is safe.
- How `singledispatch` chooses implementations.
- Why generators are lazy and usually one-shot.
- How `itertools` creates lazy pipelines.
