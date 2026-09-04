This section is about treating functions as **values**: storing them, passing them, returning them, wrapping them, partially configuring them, caching them, and composing them into lazy pipelines. Python’s functional tools are built around closures, higher-order functions, iterators, generators, `functools`, and `itertools`.[[docs.python](https://docs.python.org/3/howto/functional.html?highlight=list%20comprehension)]

# 1. Functions are objects

In Python, a function can be:

- Assigned to a variable.
- Passed to another function.
- Returned from a function.
- Stored in a list or dictionary.
- Added as an attribute of an object.
- Decorated or wrapped.

```
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

Assign the function:

```
say_hello = greet

print(say_hello("Toussaint"))
```

Output:

```
Hello, Toussaint!
```

Both names refer to the same function:

```
print(greet is say_hello)
```

Output:

```
True
```

The function itself is an object:

```
print(greet.__name__)
print(greet.__doc__)
print(callable(greet))
```

Output:

```
greet
None
True
```

This is the foundation for:

```
closures
decorators
callbacks
higher-order functions
partial application
dispatch systems
function pipelines
```

---

# 2. Nested functions

A nested function is defined inside another function.

```
def outer():
    def inner():
        return "Inside inner."

    return inner()
```

```
print(outer())
```

Output:

```
Inside inner.
```

The inner function exists only inside the execution of `outer()`.

```
def outer():
    def inner():
        return "Hello"

    return inner
```

Now `outer()` returns the function itself:

```
function = outer()

print(function())
```

Output:

```
Hello
```

A nested function is useful when:

- The helper is only relevant inside one function.
- You want to create a closure.
- You want to build a decorator.
- You want to hide implementation details.
- You want to produce a customized function.

---

# 3. Closures

A **closure** is an inner function that remembers values from its enclosing scope after the outer function has finished.

```
def make_multiplier(multiplier: int):
    def multiply(number: int) -> int:
        return number * multiplier

    return multiply
```

Create customized functions:

```
double = make_multiplier(2)
triple = make_multiplier(3)
```

Use them:

```
print(double(10))
print(triple(10))
```

Output:

```
20
30
```

The function `multiply()` remembers its own:

```
multiplier
```

even though `make_multiplier()` has already returned.

## Closure structure

```
make_multiplier(2)
        ↓
creates multiply()
        ↓
multiply remembers multiplier=2
        ↓
returns customized function double
```

Each call creates a separate closure:

```
double = make_multiplier(2)
triple = make_multiplier(3)
```

They share the same function code but remember different values.

---

# 4. Inspecting closure values

```
double = make_multiplier(2)

print(double.__closure__)
```

A closure may contain cell objects.

Inspect the remembered values:

```
print(
    [
        cell.cell_contents
        for cell in double.__closure__
    ]
)
```

Possible output:

```
[2]
```

The closure stores the value captured from the enclosing scope.

Usually, you do not need to inspect `__closure__`; it is useful for understanding how closures work internally.

---

# 5. `nonlocal`: changing a closure variable

A closure can read an enclosing variable:

```
def make_counter():
    count = 0

    def increment():
        return count + 1

    return increment
```

But this does not update `count`.

To modify a variable in the enclosing function, use:

```
nonlocal
```

```
def make_counter():
    count = 0

    def increment():
        nonlocal count

        count += 1

        return count

    return increment
```

Use:

```
counter = make_counter()

print(counter())
print(counter())
print(counter())
```

Output:

```
1
2
3
```

The closure stores state without requiring a class.

## Closure versus class

Closure:

```
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment
```

Class:

```
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count
```

Use a closure for small, private state.

Use a class when you need:

- Multiple related operations.
- Public attributes or properties.
- Inheritance.
- More complex state.
- Clear object identity.
- A larger interface.

---

# 6. Late binding in closures

This is a common closure bug.

```
functions = []

for number in range(3):
    functions.append(
        lambda: number
    )
```

Now:

```
print([function() for function in functions])
```

Output:

```
[2, 2, 2]
```

Why?

The lambdas remember the variable `number`, not its value at each loop iteration. When called later, all use the final value:

```
number == 2
```

## Fix with a default argument

```
functions = []

for number in range(3):
    functions.append(
        lambda number=number: number
    )
```

```
print([function() for function in functions])
```

Output:

```
[0, 1, 2]
```

## Fix with a factory function

```
def make_reader(value):
    def reader():
        return value

    return reader
```

```
functions = [
    make_reader(number)
    for number in range(3)
]

print([function() for function in functions])
```

Output:

```
[0, 1, 2]
```

The factory creates a separate closure for each value.

---

# 7. Higher-order functions

A higher-order function:

1. Accepts one or more functions as arguments.
2. Returns a function.
3. Or does both.

Python’s functional-programming documentation describes higher-order functions as functions that take functions as input or return new functions.[[docs.python](https://docs.python.org/3/howto/functional.html?highlight=list%20comprehension)]

## Function accepting another function

```
def apply_operation(
    operation,
    first: int,
    second: int,
):
    return operation(first, second)
```

```
def add(first, second):
    return first + second


def multiply(first, second):
    return first * second
```

```
print(apply_operation(add, 3, 4))
print(apply_operation(multiply, 3, 4))
```

Output:

```
7
12
```

## Function returning another function

```
def make_power(exponent):
    def power(number):
        return number ** exponent

    return power
```

```
square = make_power(2)
cube = make_power(3)

print(square(4))
print(cube(4))
```

Output:

```
16
64
```

---

# 8. Callbacks

A callback is a function passed to another function to be called later.

```
def process_data(data, callback):
    result = data.strip().lower()
    return callback(result)
```

```
def show_result(value):
    return f"Result: {value}"
```

```
print(process_data("  HELLO  ", show_result))
```

Output:

```
Result: hello
```

Callbacks are common in:

- Event handlers.
- Sorting.
- GUI frameworks.
- Web frameworks.
- Async tasks.
- Retry systems.
- Data pipelines.
- Plugin systems.

Example:

```
def on_success(result):
    print(f"Success: {result}")


def on_failure(error):
    print(f"Failure: {error}")


def run_operation(
    operation,
    on_success,
    on_failure,
):
    try:
        result = operation()
        on_success(result)

    except Exception as error:
        on_failure(error)
```

---

# 9. `*args`: variable positional arguments

`*args` collects extra positional arguments into a tuple.

```
def show_args(*args):
    print(args)
```

```
show_args(1, 2, 3)
```

Output:

```
(1, 2, 3)
```

The name `args` is conventional. The important syntax is:

```
*args
```

## Using `*args`

```
def add_all(*numbers: int) -> int:
    return sum(numbers)
```

```
print(add_all(1, 2, 3, 4))
```

Output:

```
10
```

Inside the function:

```
numbers
```

is a tuple:

```
(1, 2, 3, 4)
```

## No arguments

```
print(add_all())
```

Output:

```
0
```

This is because:

```
sum(())
```

returns zero.

---

# 10. `**kwargs`: variable keyword arguments

`**kwargs` collects extra keyword arguments into a dictionary.

```
def show_kwargs(**kwargs):
    print(kwargs)
```

```
show_kwargs(
    name="Toussaint",
    field="AI",
)
```

Output:

```
{
    "name": "Toussaint",
    "field": "AI",
}
```

Use it:

```
def build_profile(**attributes):
    return attributes
```

```
profile = build_profile(
    name="Toussaint",
    location="Gitega",
    interest="AI",
)

print(profile)
```

Output:

```
{
    'name': 'Toussaint',
    'location': 'Gitega',
    'interest': 'AI'
}
```

---

# 11. Combining ordinary parameters, `*args`, and `**kwargs`

```
def function(
    required,
    *args,
    keyword_only=False,
    **kwargs,
):
    ...
```

Example:

```
def inspect_call(
    first,
    *args,
    option="default",
    **kwargs,
):
    print("first:", first)
    print("args:", args)
    print("option:", option)
    print("kwargs:", kwargs)
```

```
inspect_call(
    1,
    2,
    3,
    option="custom",
    name="Toussaint",
)
```

Output:

```
first: 1
args: (2, 3)
option: custom
kwargs: {'name': 'Toussaint'}
```

Interpretation:

```
first  → 1
args   → (2, 3)
option → "custom"
kwargs → {"name": "Toussaint"}
```

---

# 12. Keyword-only arguments

Everything after `*` must be supplied by keyword.

```
def create_ticket(
    title: str,
    *,
    priority: str = "normal",
    category: str = "general",
):
    return {
        "title": title,
        "priority": priority,
        "category": category,
    }
```

Valid:

```
create_ticket(
    "Cannot log in",
    priority="high",
    category="account_access",
)
```

Invalid:

```
create_ticket(
    "Cannot log in",
    "high",
    "account_access",
)
```

Keyword-only arguments improve readability and prevent positional mistakes.

## Positional-only arguments

Everything before `/` is positional-only:

```
def divide(first, second, /, *, precision=2):
    return round(first / second, precision)
```

Valid:

```
divide(10, 3, precision=3)
```

This is invalid:

```
divide(
    first=10,
    second=3,
)
```

The `/` and `*` markers help you design clearer function APIs.

---

# 13. Argument unpacking with `*`

Suppose you have a list:

```
numbers = [1, 2, 3]
```

Pass its items as separate positional arguments:

```
def add_three(first, second, third):
    return first + second + third
```

```
print(add_three(*numbers))
```

This is equivalent to:

```
add_three(
    numbers[0],
    numbers[1],
    numbers[2],
)
```

The `*` operator unpacks an iterable.

## Unpacking in function calls

```
values = [3, 4]

print(pow(2, *values))
```

Equivalent to:

```
pow(2, 3, 4)
```

## Combining values

```
first = [1, 2]
second = [3, 4]

combined = [*first, *second]

print(combined)
```

Output:

```
[1, 2, 3, 4]
```

---

# 14. Argument unpacking with `**`

A dictionary can be unpacked into keyword arguments.

```
def create_user(name, email, active=True):
    return {
        "name": name,
        "email": email,
        "active": active,
    }
```

```
data = {
    "name": "Toussaint",
    "email": "toussaint@example.com",
    "active": True,
}
```

```
user = create_user(**data)

print(user)
```

This is equivalent to:

```
create_user(
    name=data["name"],
    email=data["email"],
    active=data["active"],
)
```

## Dictionary merging

```
defaults = {
    "temperature": 0.7,
    "max_tokens": 500,
}

custom = {
    "temperature": 0.2,
}

config = {
    **defaults,
    **custom,
}

print(config)
```

Output:

```
{
    "temperature": 0.2,
    "max_tokens": 500
}
```

Later keys override earlier keys.

---

# 15. Forwarding arguments

A wrapper can forward any arguments:

```
def log_call(function):
    def wrapper(*args, **kwargs):
        print(
            f"Calling {function.__name__}"
        )

        return function(*args, **kwargs)

    return wrapper
```

This works for functions with different signatures:

```
@log_call
def add(first, second):
    return first + second
```

```
@log_call
def greet(name, title=""):
    return f"{title} {name}".strip()
```

The wrapper accepts everything and forwards it.

For typed decorators, use `ParamSpec`:

```
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar
```

```
P = ParamSpec("P")
R = TypeVar("R")
```

```
def log_call(
    function: Callable[P, R],
) -> Callable[P, R]:
    @wraps(function)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        print(
            f"Calling {function.__name__}"
        )

        return function(*args, **kwargs)

    return wrapper
```

This preserves the wrapped function’s parameter and return types for static checkers.

# 16. Decorators: the fundamental transformation

A decorator is a callable that receives a function or class and returns a replacement.

```
def uppercase(function):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        return result.upper()

    return wrapper
```

Apply it:

```
@uppercase
def greet():
    return "hello"
```

This is equivalent to:

```
def greet():
    return "hello"

greet = uppercase(greet)
```

Call it:

```
print(greet())
```

Output:

```
HELLO
```

The decorator did not modify the original function’s source code. It replaced the name with a wrapped function.

---

# 17. `functools.wraps`

Always use `wraps` in reusable decorators.

```
from functools import wraps
```

```
def uppercase(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        return result.upper()

    return wrapper
```

Why?

```
@uppercase
def greet():
    """Return a greeting."""
    return "hello"
```

Without `wraps`:

```
greet.__name__ == "wrapper"
greet.__doc__ is None
```

With `wraps`:

```
greet.__name__ == "greet"
greet.__doc__ == "Return a greeting."
```

`wraps` copies metadata and sets `__wrapped__`, which helps introspection and debugging.

---

# 18. Decorator patterns

## Logging decorator

```
from functools import wraps


def log_calls(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(
            f"START {function.__name__}"
        )

        result = function(*args, **kwargs)

        print(
            f"END {function.__name__}"
        )

        return result

    return wrapper
```

## Timing decorator

```
from functools import wraps
from time import perf_counter


def measure_time(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = perf_counter()

        try:
            return function(*args, **kwargs)

        finally:
            elapsed = perf_counter() - start

            print(
                f"{function.__name__}: "
                f"{elapsed:.6f}s"
            )

    return wrapper
```

## Validation decorator

```
from functools import wraps


def require_non_empty_text(function):
    @wraps(function)
    def wrapper(text, *args, **kwargs):
        if not isinstance(text, str):
            raise TypeError(
                "Text must be a string."
            )

        if not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        return function(
            text.strip(),
            *args,
            **kwargs,
        )

    return wrapper
```

## Retry decorator

```
from functools import wraps
from time import sleep


def retry(attempts, delay=1):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(attempts):
                try:
                    return function(
                        *args,
                        **kwargs,
                    )

                except ConnectionError as error:
                    last_error = error

                    if attempt < attempts - 1:
                        sleep(delay)

            raise last_error

        return wrapper

    return decorator
```

Use:

```
@retry(attempts=3, delay=2)
def call_provider():
    ...
```

Only retry errors that are genuinely transient.

---

# 19. Parameterized decorators

A normal decorator:

```
@decorator
def function():
    ...
```

means:

```
function = decorator(function)
```

A parameterized decorator:

```
@decorator(option)
def function():
    ...
```

means:

```
function = decorator(option)(function)
```

This requires three nested levels:

```
def decorator_factory(option):
    def decorator(function):
        def wrapper(*args, **kwargs):
            ...
        return wrapper

    return decorator
```

Example:

```
from functools import wraps


def repeat(times: int):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = None

            for _ in range(times):
                result = function(
                    *args,
                    **kwargs,
                )

            return result

        return wrapper

    return decorator
```

```
@repeat(3)
def greet(name):
    print(f"Hello, {name}!")
```

```
greet("Toussaint")
```

Output:

```
Hello, Toussaint!
Hello, Toussaint!
Hello, Toussaint!
```

---

# 20. Decorator factories that support optional configuration

You may want both forms:

```
@log_calls
def function():
    ...
```

and:

```
@log_calls(level="debug")
def function():
    ...
```

One pattern:

```
from functools import wraps


def log_calls(function=None, *, level="info"):
    def decorator(target):
        @wraps(target)
        def wrapper(*args, **kwargs):
            print(
                f"[{level.upper()}] "
                f"{target.__name__}"
            )

            return target(*args, **kwargs)

        return wrapper

    if function is not None:
        return decorator(function)

    return decorator
```

Use without configuration:

```
@log_calls
def greet():
    return "Hello"
```

Use with configuration:

```
@log_calls(level="debug")
def calculate():
    return 42
```

This pattern is flexible but more complex. Prefer separate decorators when that improves readability.

---

# 21. Class decorators

A class decorator receives a class and returns a class.

```
def add_version(cls):
    cls.version = "1.0.0"
    return cls
```

```
@add_version
class TicketService:
    pass
```

Equivalent:

```
class TicketService:
    pass

TicketService = add_version(TicketService)
```

Use:

```
print(TicketService.version)
```

Output:

```
1.0.0
```

## Plugin registration

```
PLUGINS = {}
```

```
def register_plugin(name):
    def decorator(cls):
        PLUGINS[name] = cls
        return cls

    return decorator
```

```
@register_plugin("sentiment")
class SentimentPlugin:
    def run(self, text):
        return "neutral"
```

```
@register_plugin("ticket")
class TicketPlugin:
    def run(self, text):
        return "general"
```

Use:

```
plugin_class = PLUGINS["ticket"]
plugin = plugin_class()

print(plugin.run("I cannot log in"))
```

This is useful for:

- AI tools.
- Model providers.
- CLI commands.
- Plugin systems.
- Serializers.
- Framework registration.

---

# 22. Decorator order

```
@outer
@inner
def function():
    ...
```

means:

```
function = outer(inner(function))
```

The decorator closest to the function is applied first.

Example:

```
from functools import wraps


def add_prefix(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return "Result: " + function(
            *args,
            **kwargs,
        )

    return wrapper
```

```
def uppercase(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(
            *args,
            **kwargs,
        ).upper()

    return wrapper
```

```
@add_prefix
@uppercase
def message():
    return "hello"
```

Equivalent:

```
message = add_prefix(
    uppercase(message)
)
```

Output:

```
Result: HELLO
```

Reverse:

```
@uppercase
@add_prefix
def message():
    return "hello"
```

Output:

```
RESULT: HELLO
```

Order matters whenever decorators:

- Transform values.
- Catch exceptions.
- Authenticate.
- Log.
- Cache.
- Retry.
- Modify arguments.
- Change control flow.

# 23. `functools.partial`

`partial` pre-fills arguments and returns a new callable.

```
from functools import partial
```

```
def power(base, exponent):
    return base ** exponent
```

```
square = partial(
    power,
    exponent=2,
)

cube = partial(
    power,
    exponent=3,
)
```

```
print(square(5))
print(cube(5))
```

Output:

```
25
125
```

## `partial` versus closure

With a closure:

```
def make_square():
    def square(value):
        return value ** 2

    return square
```

With `partial`:

```
square = partial(
    power,
    exponent=2,
)
```

Use `partial` when you are simply pre-filling existing arguments.

Use a closure when you need custom logic around the captured value.

---

# 24. `lru_cache`

`lru_cache` remembers previous results.

```
from functools import lru_cache


@lru_cache(maxsize=128)
def fibonacci(number: int) -> int:
    if number < 2:
        return number

    return (
        fibonacci(number - 1)
        + fibonacci(number - 2)
    )
```

```
print(fibonacci(30))
print(fibonacci.cache_info())
```

The arguments must be hashable:

```
fibonacci(30)
```

works.

This may not:

```
fibonacci([1, 2, 3])
```

because lists are unhashable.

## Cache methods

```
fibonacci.cache_info()
fibonacci.cache_clear()
```

Use caching for:

- Pure calculations.
- Repeated parsing.
- Static configuration.
- Deterministic model metadata.
- Expensive recursive algorithms.
- Stable lookup functions.

Avoid caching:

- Current database state.
- Time-dependent results.
- Random functions.
- Functions with side effects.
- User-sensitive data without careful isolation.

For async functions, normal `lru_cache` caches the coroutine object, not necessarily the awaited result. Use an async-aware caching strategy instead.

---

# 25. `reduce`

`reduce` combines an iterable into one value.

```
from functools import reduce
import operator
```

```
numbers = [1, 2, 3, 4]

total = reduce(
    operator.add,
    numbers,
)

print(total)
```

Output:

```
10
```

With an initializer:

```
total = reduce(
    operator.add,
    numbers,
    100,
)

print(total)
```

Output:

```
110
```

The initializer is used when the iterable is empty and becomes the starting accumulator.

## Use a named function for clarity

```
def combine_scores(
    accumulated: float,
    current: float,
) -> float:
    return accumulated + current
```

```
total = reduce(
    combine_scores,
    [0.8, 0.9, 0.95],
)
```

For ordinary operations, prefer clearer built-ins:

```
sum(numbers)
max(numbers)
min(numbers)
```

`reduce` is best when the accumulation operation is domain-specific or naturally functional.

---

# 26. `singledispatch`

`singledispatch` selects an implementation using the type of the first argument.

```
from functools import singledispatch
```

```
@singledispatch
def serialize(value):
    raise TypeError(
        f"Unsupported type: {type(value).__name__}"
    )
```

```
@serialize.register
def _(value: str):
    return {
        "type": "string",
        "value": value,
    }
```

```
@serialize.register
def _(value: int):
    return {
        "type": "integer",
        "value": value,
    }
```

```
@serialize.register
def _(value: list):
    return {
        "type": "list",
        "value": [
            serialize(item)
            for item in value
        ],
    }
```

```
print(serialize("hello"))
print(serialize(42))
print(serialize(["AI", 2026]))
```

This is useful when one function needs type-specific behavior.

Use ordinary polymorphism or a protocol when the behavior belongs naturally to the objects themselves.

# 27. Advanced iteration patterns

## Lazy map

```
names = ["alice", "bob", "carol"]

lower_names = map(
    str.lower,
    names,
)

print(list(lower_names))
```

Output:

```
['alice', 'bob', 'carol']
```

In modern Python, a generator expression is often clearer:

```
lower_names = (
    name.lower()
    for name in names
)
```

## Lazy filter

```
numbers = range(10)

even_numbers = filter(
    lambda number: number % 2 == 0,
    numbers,
)

print(list(even_numbers))
```

Equivalent generator expression:

```
even_numbers = (
    number
    for number in numbers
    if number % 2 == 0
)
```

For simple transformations, comprehensions are often most readable:

```
even_numbers = [
    number
    for number in numbers
    if number % 2 == 0
]
```

Choose based on memory and reuse needs.

---

# 28. `itertools.chain`

```
from itertools import chain
```

```
batches = [
    ["T-001", "T-002"],
    ["T-003"],
    ["T-004", "T-005"],
]

all_tickets = chain.from_iterable(
    batches
)

for ticket_id in all_tickets:
    print(ticket_id)
```

Output:

```
T-001
T-002
T-003
T-004
T-005
```

This is lazy and avoids creating a separate flattened list.

---

# 29. `itertools.islice`

```
from itertools import islice
```

```
first_ten = islice(
    range(1_000_000),
    10,
)

print(list(first_ten))
```

Output:

```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Use it to limit infinite or large iterators:

```
from itertools import count, islice

sample = islice(
    count(1),
    5,
)

print(list(sample))
```

Output:

```
[1, 2, 3, 4, 5]
```

---

# 30. `itertools.groupby`

`groupby` groups consecutive items sharing a key.

```
from itertools import groupby
```

```
tickets = [
    {"category": "billing", "id": "T-001"},
    {"category": "billing", "id": "T-002"},
    {"category": "technical", "id": "T-003"},
]
```

```
for category, group in groupby(
    tickets,
    key=lambda ticket: ticket["category"],
):
    print(
        category,
        list(group),
    )
```

Output:

```
billing [
    {'category': 'billing', 'id': 'T-001'},
    {'category': 'billing', 'id': 'T-002'}
]
technical [
    {'category': 'technical', 'id': 'T-003'}
]
```

Sort first if equal keys are scattered:

```
tickets = sorted(
    tickets,
    key=lambda ticket: ticket["category"],
)
```

# 31. `itertools.product` for experiments

```
from itertools import product
```

```
models = [
    "local-model",
    "cloud-model",
]

temperatures = [
    0.0,
    0.5,
    1.0,
]

experiments = product(
    models,
    temperatures,
)

for model, temperature in experiments:
    print(model, temperature)
```

Output:

```
local-model 0.0
local-model 0.5
local-model 1.0
cloud-model 0.0
cloud-model 0.5
cloud-model 1.0
```

This is valuable for model evaluation grids.

# 32. `itertools.accumulate`

```
from itertools import accumulate
```

```
expenses = [100, 250, 50]

running_total = accumulate(expenses)

print(list(running_total))
```

Output:

```
[100, 350, 400]
```

Use it for:

- Budget tracking.
- Cumulative token usage.
- Running performance.
- Incremental resource consumption.

# 33. Advanced pipeline example

```
from dataclasses import dataclass
from itertools import chain, islice
from collections import Counter
from functools import partial
```

```
@dataclass
class Ticket:
    ticket_id: str
    text: str
    category: str
```

Lazy normalization:

```
def normalize_ticket(
    ticket: Ticket,
) -> Ticket:
    return Ticket(
        ticket_id=ticket.ticket_id,
        text=ticket.text.strip().lower(),
        category=ticket.category,
    )
```

Filter:

```
def is_high_priority(
    ticket: Ticket,
) -> bool:
    return "urgent" in ticket.text
```

Create batches:

```
batches = [
    [
        Ticket("T-001", "Urgent login issue", "access"),
        Ticket("T-002", "Invoice question", "billing"),
    ],
    [
        Ticket("T-003", "Urgent payment failure", "billing"),
        Ticket("T-004", "Feature request", "general"),
    ],
]
```

Pipeline:

```
all_tickets = chain.from_iterable(batches)

normalized = map(
    normalize_ticket,
    all_tickets,
)

urgent = filter(
    is_high_priority,
    normalized,
)

first_urgent = islice(urgent, 2)

urgent_tickets = list(first_urgent)
```

Count categories:

```
category_counts = Counter(
    ticket.category
    for ticket in urgent_tickets
)

print(urgent_tickets)
print(category_counts)
```

This pipeline is:

```
nested batches
    ↓ chain
all tickets
    ↓ map
normalized tickets
    ↓ filter
urgent tickets
    ↓ islice
first two
    ↓ Counter
category statistics
```

Nothing is processed until the pipeline is consumed by:

```
list(...)
```

or:

```
Counter(...)
```

# 34. When not to use functional tools

Functional tools are useful, but readability comes first.

Less readable:

```
result = reduce(
    lambda a, b: a + f(g(b)),
    values,
)
```

Often clearer:

```
result = 0

for value in values:
    transformed = g(value)
    result += f(transformed)
```

Use functional tools when they make the operation clearer:

```
total = sum(values)
```

```
names = [
    user.name
    for user in users
]
```

```
for ticket in filter(is_high_priority, tickets):
    ...
```

Do not force every operation into:

```
map → filter → reduce
```

Python supports both functional and imperative styles. Choose the form that communicates the algorithm best.

# 35. Practice exercises

## Exercise 1: Closure

Create:

```
make_discount(percent)
```

It should return a function that calculates the discounted price.

Example:

```
discount_20 = make_discount(20)

print(discount_20(100))
```

Expected:

```
80.0
```

## Exercise 2: Decorator

Create:

```
@validate_positive
```

It should reject numeric arguments that are less than or equal to zero.

## Exercise 3: `*args` and `**kwargs`

Create:

```
def summarize_call(function, *args, **kwargs):
    ...
```

It should print the function name, positional arguments, keyword arguments, and result.

## Exercise 4: Partial

Create a generic:

```
send_notification(channel, recipient, message)
```

Then create:

```
send_email
send_sms
```

using `partial`.

## Exercise 5: Lazy pipeline

Given a generator of ticket dictionaries:

```
tickets = (
    {
        "id": "T-001",
        "priority": "high",
    },
    ...
)
```

Build a lazy pipeline that:

1. Keeps only high-priority tickets.
2. Extracts ticket IDs.
3. Takes the first three.
4. Returns a list.

## Exercise 6: Experiment grid

Use `itertools.product()` to generate combinations of:

```
models = ["local", "cloud"]
temperatures = [0.0, 0.5, 1.0]
```

## Exercise 7: Cached function

Create a cached recursive Fibonacci function and inspect:

```
cache_info()
```

# 36. Exercise answers

## Exercise 1 answer

```
def make_discount(percent: float):
    multiplier = 1 - percent / 100

    def apply_discount(price: float) -> float:
        return price * multiplier

    return apply_discount
```

```
discount_20 = make_discount(20)

print(discount_20(100))
```

Output:

```
80.0
```

## Exercise 2 answer

```
from functools import wraps


def validate_positive(function):
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

```
@validate_positive
def square_root_input(value):
    return value ** 0.5
```

## Exercise 3 answer

```
from functools import wraps


def summarize_call(function, *args, **kwargs):
    print("Function:", function.__name__)
    print("Arguments:", args)
    print("Keyword arguments:", kwargs)

    result = function(
        *args,
        **kwargs,
    )

    print("Result:", result)

    return result
```

```
def add(first, second):
    return first + second


summarize_call(
    add,
    2,
    3,
)
```

## Exercise 4 answer

```
from functools import partial
```

```
def send_notification(
    channel,
    recipient,
    message,
):
    return (
        f"{channel} notification to "
        f"{recipient}: {message}"
    )
```

```
send_email = partial(
    send_notification,
    "email",
)

send_sms = partial(
    send_notification,
    "sms",
)
```

```
print(
    send_email(
        "user@example.com",
        "Report ready.",
    )
)

print(
    send_sms(
        "+25700000000",
        "Code: 123456",
    )
)
```

## Exercise 5 answer

```
from itertools import islice
```

```
def is_high_priority(ticket):
    return ticket["priority"] == "high"


def ticket_id(ticket):
    return ticket["id"]
```

```
high_priority_ids = islice(
    map(
        ticket_id,
        filter(
            is_high_priority,
            tickets,
        ),
    ),
    3,
)

result = list(high_priority_ids)
```

A generator expression may be easier to read:

```
result = list(
    ticket["id"]
    for ticket in tickets
    if ticket["priority"] == "high"
)[:3]
```

The first version is fully lazy until the final `list`.

## Exercise 6 answer

```
from itertools import product
```

```
experiments = product(
    ["local", "cloud"],
    [0.0, 0.5, 1.0],
)

for model, temperature in experiments:
    print({
        "model": model,
        "temperature": temperature,
    })
```

## Exercise 7 answer

```
from functools import lru_cache
```

```
@lru_cache(maxsize=None)
def fibonacci(number: int) -> int:
    if number < 2:
        return number

    return (
        fibonacci(number - 1)
        + fibonacci(number - 2)
    )
```

```
print(fibonacci(35))
print(fibonacci.cache_info())
```

# 37. Final mental model

## Closures

```
def factory(configuration):
    def function(value):
        ...
    return function
```

Use when a function should remember private configuration or state.

## Decorators

```
@decorator
def function():
    ...
```

Use to add reusable behavior around functions or classes.

## `*args` and `**kwargs`

```
def wrapper(*args, **kwargs):
    return function(*args, **kwargs)
```

Use to collect and forward flexible arguments.

## Higher-order functions

```
def apply(function, value):
    return function(value)
```

Use functions as data.

## `functools`

```
partial
lru_cache
cache
wraps
singledispatch
reduce
```

Use for function specialization, caching, metadata preservation, dispatch, and reduction.

## Generators

```
def generate():
    yield value
```

Use for lazy, one-at-a-time data production.

## `itertools`

```
chain
islice
groupby
product
accumulate
```

Use to build lazy iteration pipelines.

The most important practical rule is:

```
Use generators when data may be large.
Use itertools to compose lazy operations.
Use functools to configure and reuse functions.
Use decorators for cross-cutting behavior.
Use closures for small private state.
Use *args/**kwargs for flexible wrappers and APIs.
```

For an AI-engineering projects, these concepts support efficient ticket streams, experiment grids, retry and timing decorators, configurable model providers, cached computations, tool registries, batch preprocessing, and memory-efficient evaluation pipelines.[[docs.python](https://docs.python.org/3/library/itertools.html)][[docs.python](https://docs.python.org/3/howto/functional.html)]
