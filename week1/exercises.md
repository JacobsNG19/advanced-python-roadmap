# Advanced Functions & Functional Tools — Exercises

## Instructions

Solve each problem independently. Choose your own implementation. The questions do not require a particular programming technique unless the requirement is part of the behavior being tested.

Write your code in a separate Python file and test it after every exercise.

---

## Exercise 1 — Configurable price calculation

Create `make_price_calculator(discount_percent)`.

It must return a callable that accepts a price and returns the price after applying the configured discount.

Requirements:

- A discount of `20` means a 20% reduction.
- The discount must be between `0` and `100`.
- The price cannot be negative.

Expected behavior:

```python
calculator = make_price_calculator(20)

assert calculator(100) == 80
assert calculator(50) == 40
```

---

## Exercise 2 — Independent counters

Create `make_counter(start=0)`.

Each returned counter must maintain its own current value.

Expected behavior:

```python
first = make_counter(0)
second = make_counter(10)

assert first() == 1
assert first() == 2
assert second() == 11
assert first() == 3
```

---

## Exercise 3 — Text formatter factory

Create `make_formatter(prefix, suffix)`.

The returned callable must surround text with the configured prefix and suffix.

Expected behavior:

```python
bracket_formatter = make_formatter("[", "]")

assert bracket_formatter("ready") == "[ready]"
```

---

## Exercise 4 — Operation runner

Create `run_operation(operation, first, second)`.

It must execute the supplied operation using the two numbers and return the result.

Expected behavior:

```python
assert run_operation(lambda a, b: a + b, 2, 3) == 5
assert run_operation(lambda a, b: a * b, 2, 3) == 6
```

---

## Exercise 5 — Transform a sequence

Create `transform_all(values, transform)`.

It must return a new list containing the transformed version of every value.

Expected behavior:

```python
assert transform_all([1, 2, 3], lambda x: x * 2) == [2, 4, 6]
assert transform_all(["a", "b"], str.upper) == ["A", "B"]
```

---

## Exercise 6 — Flexible statistics

Create `statistics(*numbers)`.

Return a dictionary containing:

```text
count
minimum
maximum
total
average
```

For no numbers, raise `ValueError`.

Expected behavior:

```python
result = statistics(10, 20, 30)

assert result["count"] == 3
assert result["minimum"] == 10
assert result["maximum"] == 30
assert result["total"] == 60
assert result["average"] == 20
```

---

## Exercise 7 — Profile builder

Create `build_profile(**attributes)`.

It must return a copy of the supplied keyword arguments. Changing the returned dictionary must not change any dictionary that was used to supply the values.

Expected behavior:

```python
profile = build_profile(
    name="Toussaint",
    field="AI Engineering",
)

assert profile["name"] == "Toussaint"
assert profile["field"] == "AI Engineering"
```

---

## Exercise 8 — Argument forwarding

Create `call_with_arguments(function, positional, keywords)`.

- `positional` will be a list or tuple.
- `keywords` will be a dictionary.
- Call `function` using both collections.
- Return the result.

Expected behavior:

```python
def create_user(name, email, active=True):
    return name, email, active


result = call_with_arguments(
    create_user,
    ["Toussaint", "toussaint@example.com"],
    {"active": True},
)

assert result == (
    "Toussaint",
    "toussaint@example.com",
    True,
)
```

---

## Exercise 9 — Logging wrapper

Create `with_logging(function)`.

The returned callable must:

- Print the wrapped function's name before execution.
- Execute the function with any positional and keyword arguments.
- Return the original result.
- Preserve the original function's name and docstring.

Expected behavior:

```python
@with_logging
def add(a, b):
    """Add two values."""
    return a + b


assert add(2, 3) == 5
assert add.__name__ == "add"
assert add.__doc__ == "Add two values."
```

---

## Exercise 10 — Positive first argument

Create `require_positive(function)`.

The returned callable must reject a first numeric argument that is less than or equal to zero.

Expected behavior:

```python
@require_positive
def square_root_input(value):
    return value ** 0.5


assert square_root_input(9) == 3
```

The following calls must raise `ValueError`:

```python
square_root_input(0)
square_root_input(-1)
```

---

## Exercise 11 — Configurable repetition

Create `repeat(times)`.

It must produce a decorator that executes a function the requested number of times and returns the final result.

Expected behavior:

```python
calls = []


@repeat(3)
def record():
    calls.append("called")
    return len(calls)


assert record() == 3
assert len(calls) == 3
```

---

## Exercise 12 — Retry temporary failures

Create `retry(attempts)`.

It must produce a decorator that retries a function when it raises `ConnectionError`.

Requirements:

- Return immediately after a successful call.
- Re-raise the final `ConnectionError` if every attempt fails.
- Do not retry unrelated exception types.

---

## Exercise 13 — Class registration

Create `register_plugin(name)`.

It must produce a class decorator that stores plugin classes in a registry.

Expected behavior:

```python
@register_plugin("search")
class SearchPlugin:
    def run(self, text):
        return f"Searching: {text}"
```

The class must be retrievable from the registry using the name `"search"`.

---

## Exercise 14 — Specialized notification functions

Create:

```python
send_notification(channel, recipient, message)
```

Then create specialized callables named:

```text
send_email
send_sms
```

They must automatically provide the appropriate channel while allowing the caller to provide the recipient and message.

Expected behavior:

```python
assert send_email(
    "user@example.com",
    "Report ready",
) == "email to user@example.com: Report ready"
```

---

## Exercise 15 — Cached Fibonacci

Create a function `fibonacci(number)` that calculates Fibonacci values.

Requirements:

- `fibonacci(0) == 0`.
- `fibonacci(1) == 1`.
- `fibonacci(10) == 55`.
- Repeated calls should reuse previous results.

Expose a way to inspect and clear the stored results.

---

## Exercise 16 — Type-specific serialization

Create `serialize(value)` with different results for:

- `str`
- `int`
- `list`

Expected behavior:

```python
assert serialize("hello") == {
    "type": "string",
    "value": "hello",
}

assert serialize(42) == {
    "type": "integer",
    "value": 42,
}
```

Unsupported types must raise `TypeError`.

---

## Exercise 17 — Lazy positive values

Create `positive_values(values)`.

It must produce positive values one at a time and ignore zero and negative values.

Expected behavior:

```python
result = positive_values([-2, 0, 3, -1, 5])

assert list(result) == [3, 5]
```

---

## Exercise 18 — Lazy text pipeline

Create a pipeline that processes text values as follows:

1. Remove surrounding whitespace.
2. Ignore empty values.
3. Convert remaining values to lowercase.

Expected behavior:

```python
values = ["  Python  ", "", "  AI  "]

assert list(process_text(values)) == [
    "python",
    "ai",
]
```

The pipeline should not create unnecessary intermediate collections.

---

## Exercise 19 — Flatten batches and limit results

Given nested batches, return only the first `limit` items in their original order.

Expected behavior:

```python
batches = [
    ["T-001", "T-002"],
    ["T-003", "T-004"],
    ["T-005"],
]

assert first_items(batches, 3) == [
    "T-001",
    "T-002",
    "T-003",
]
```

---

## Exercise 20 — Group sorted records

Given records sorted by category, return a dictionary mapping each category to its records.

Expected behavior:

```python
records = [
    {"id": "T-001", "category": "billing"},
    {"id": "T-002", "category": "billing"},
    {"id": "T-003", "category": "technical"},
]

result = group_by_category(records)

assert [item["id"] for item in result["billing"]] == [
    "T-001",
    "T-002",
]
```

---

## Exercise 21 — Experiment combinations

Given model names and temperatures, produce every experiment configuration.

Expected behavior:

```python
models = ["local", "cloud"]
temperatures = [0.0, 0.5]

assert experiment_grid(models, temperatures) == [
    {"model": "local", "temperature": 0.0},
    {"model": "local", "temperature": 0.5},
    {"model": "cloud", "temperature": 0.0},
    {"model": "cloud", "temperature": 0.5},
]
```

---

## Exercise 22 — Running totals

Given a sequence of expenses, produce the cumulative total after every expense.

Expected behavior:

```python
assert running_totals([100, 250, 50]) == [
    100,
    350,
    400,
]
```

---

## Exercise 23 — Lazy ticket pipeline

Build a pipeline that:

1. Receives ticket dictionaries.
2. Keeps only high-priority tickets.
3. Extracts ticket IDs.
4. Returns no more than a requested limit.

Expected behavior:

```python
tickets = [
    {"id": "T-001", "priority": "low"},
    {"id": "T-002", "priority": "high"},
    {"id": "T-003", "priority": "high"},
    {"id": "T-004", "priority": "normal"},
    {"id": "T-005", "priority": "high"},
]

assert high_priority_ids(tickets, 2) == [
    "T-002",
    "T-003",
]
```

---

## Exercise 24 — Final mini-project

Build a functional ticket toolkit with the following behavior:

1. Generate sequential ticket IDs with a configurable prefix.
2. Create tickets with a title, category, and priority.
3. Create a specialized way to make high-priority tickets.
4. Process records lazily.
5. Filter high-priority tickets.
6. Count categories.
7. Add logging around the category-counting operation.

Expected final behavior:

```python
first_id = next_ticket_id()
second_id = next_ticket_id()

assert first_id == "T-001"
assert second_id == "T-002"

urgent = create_urgent_ticket(
    "Production outage",
    category="technical",
)

assert urgent["priority"] == "high"
```

# Practice rules

1. Solve the questions in order.
2. Do not look at the solutions until you have attempted the problem.
3. Add at least one edge-case test to every exercise.
4. Run a type checker when the exercise includes function interfaces.
5. Rewrite any solution you copied until you can explain every line.
