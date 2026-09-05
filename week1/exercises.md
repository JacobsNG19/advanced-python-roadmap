Metaprogramming means writing code that **examines, creates, or modifies other code at runtime**. In Python, the practical tools you need are `inspect`, `getattr`/`setattr`, decorators, dynamic imports, registries, descriptors, `__init_subclass__`, and carefully chosen design patterns. Use them to build flexible libraries and frameworks—but prefer ordinary functions and classes when they are sufficient.

# 1. Introspection

Introspection means examining live Python objects while the program is running. The `inspect` module can examine modules, classes, functions, methods, signatures, source code, tracebacks, frames, and code objects. [docs.python](https://docs.python.org/3/library/inspect.html)

## `type()` and `isinstance()`

```python
value = "TrustDesk"

print(type(value))
print(isinstance(value, str))
```

Output:

```text
<class 'str'>
True
```

Use:

```python
isinstance(value, SomeClass)
```

when you need to know whether an object supports a specific class relationship.

Avoid excessive type checks when duck typing is enough:

```python
def export(item):
    return item.export()
```

## `dir()`

`dir()` shows many available attribute names:

```python
class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}"


user = User("Toussaint")

print(dir(user))
```

This is useful for exploration, but `dir()` is not a complete or guaranteed list of everything accessible on an object.

## `vars()` and `__dict__`

```python
print(vars(user))
```

Output:

```python
{'name': 'Toussaint'}
```

This is usually equivalent to:

```python
print(user.__dict__)
```

For classes:

```python
print(User.__dict__)
```

You may see:

```python
{
    '__module__': '__main__',
    '__init__': <function ...>,
    'greet': <function ...>,
    '__dict__': <attribute ...>,
    '__weakref__': <attribute ...>,
    '__doc__': None,
}
```

`__dict__` shows directly stored attributes, but it does not fully represent behavior supplied by descriptors, base classes, or metaclasses.

## `hasattr()` and `getattr()`

```python
if hasattr(user, "greet"):
    print(user.greet())
```

Retrieve dynamically:

```python
method = getattr(user, "greet")
print(method())
```

With a default:

```python
email = getattr(
    user,
    "email",
    "not-provided",
)

print(email)
```

This is safer than:

```python
user.email
```

when the attribute may not exist.

## Dynamic attributes

```python
class Config:
    pass


config = Config()

setattr(config, "model_name", "local-model")

print(getattr(config, "model_name"))
```

This is equivalent to:

```python
config.model_name = "local-model"
```

Use dynamic attributes for:

- Plugin metadata.
- Framework-generated fields.
- Configuration objects.
- Serialization systems.
- Adapters for dynamic APIs.

Avoid using them for ordinary business logic because strings such as:

```python
"model_name"
```

are easier to mistype and harder for static type checkers to understand.

# 2. `inspect`

## Inspect a signature

```python
import inspect


def create_ticket(
    title: str,
    priority: str = "normal",
) -> dict:
    return {
        "title": title,
        "priority": priority,
    }


signature = inspect.signature(
    create_ticket
)

print(signature)
```

Output:

```text
(title: str, priority: str = 'normal') -> dict
```

Inspect parameters:

```python
for name, parameter in signature.parameters.items():
    print(
        name,
        parameter.annotation,
        parameter.default,
        parameter.kind,
    )
```

This is useful for:

- CLI generation.
- Dependency injection.
- API validation.
- Automatic documentation.
- Tool schemas for AI agents.
- Testing utilities.

## Binding arguments

```python
arguments = signature.bind(
    "Cannot log in",
    priority="high",
)

print(arguments.arguments)
```

Output:

```python
{
    'title': 'Cannot log in',
    'priority': 'high'
}
```

Apply default values:

```python
arguments.apply_defaults()
```

This is useful when building a framework that wants to validate or normalize function calls before executing them.

## Inspect members

```python
members = inspect.getmembers(user)

for name, value in members[:10]:
    print(name, value)
```

Filter methods:

```python
methods = inspect.getmembers(
    user,
    predicate=inspect.ismethod,
)

print(methods)
```

`inspect.getmembers()` returns sorted `(name, value)` pairs and can filter members with a predicate. [docs.python](https://docs.python.org/3/library/inspect.html)

## `getmembers_static()`

Normal inspection may trigger:

- Descriptors.
- `__getattr__`.
- `__getattribute__`.

Use:

```python
inspect.getmembers_static(obj)
```

when you want to inspect attributes without triggering dynamic lookup. This is useful for framework tooling and objects with unusual attribute behavior. [docs.python](https://docs.python.org/3/library/inspect.html)

## Source and documentation

```python
print(inspect.getdoc(create_ticket))
print(inspect.getsource(create_ticket))
```

Source may be unavailable for:

- Built-in functions.
- Dynamically generated functions.
- Interactive definitions.
- Compiled extensions.

Do not build critical application behavior around source-code inspection.

# 3. Dynamic imports

Use `importlib.import_module()` to import a module from a string.

```python
import importlib


module = importlib.import_module("json")

print(module.dumps({
    "status": "ok",
}))
```

The `importlib` documentation provides `import_module()` for programmatic imports. [docs.python](https://docs.python.org/3/library/importlib.html)

## Plugin loading

```python
def load_plugin(
    module_name: str,
    class_name: str,
):
    module = importlib.import_module(
        module_name
    )

    plugin_class = getattr(
        module,
        class_name,
    )

    return plugin_class()
```

Use:

```python
plugin = load_plugin(
    "trustdesk.plugins.sentiment",
    "SentimentPlugin",
)
```

This enables plugin architectures:

```text
configuration → module path → class name → loaded implementation
```

## Security warning

Never import arbitrary user-provided module paths without validation.

Dangerous:

```python
module_name = input("Module: ")
importlib.import_module(module_name)
```

A dynamic import may load and execute code.

Use:

- An allowlist of modules.
- Signed plugins.
- Trusted plugin directories.
- Package metadata entry points.
- Permissions and sandboxing where appropriate.

# 4. Dynamic dispatch

Instead of writing:

```python
if command == "add":
    add_ticket()
elif command == "list":
    list_tickets()
```

use a dispatch dictionary:

```python
def add_ticket():
    return "Ticket added."


def list_tickets():
    return "Tickets listed."


COMMANDS = {
    "add": add_ticket,
    "list": list_tickets,
}
```

```python
command = "add"

handler = COMMANDS.get(command)

if handler is None:
    raise ValueError(
        f"Unknown command: {command}"
    )

print(handler())
```

This is a simple, Pythonic form of metaprogramming.

For CLI tools:

```python
args.function(args)
```

using `argparse.set_defaults()` is another dispatch-table pattern.

# 5. Registries

A registry maps names to implementations.

```python
TOOLS = {}
```

```python
def register_tool(name):
    def decorator(function):
        TOOLS[name] = function
        return function

    return decorator
```

Register functions:

```python
@register_tool("search")
def search_tool(query):
    return f"Searching for {query}"
```

```python
@register_tool("summarize")
def summarize_tool(text):
    return f"Summary of {text}"
```

Use:

```python
tool = TOOLS["search"]

print(tool("Python decorators"))
```

Output:

```text
Searching for Python decorators
```

This pattern is useful for:

- Agent tools.
- CLI commands.
- Model providers.
- Serializers.
- Plugin systems.
- Event handlers.
- Experiment strategies.

## Class registry with `__init_subclass__`

```python
class Plugin:
    registry = {}

    def __init_subclass__(
        cls,
        plugin_name=None,
        **kwargs,
    ):
        super().__init_subclass__(**kwargs)

        if plugin_name is None:
            raise TypeError(
                "plugin_name is required."
            )

        Plugin.registry[plugin_name] = cls
```

Register subclasses:

```python
class TicketPlugin(
    Plugin,
    plugin_name="ticket",
):
    def run(self, text):
        return "ticket"
```

```python
class SentimentPlugin(
    Plugin,
    plugin_name="sentiment",
):
    def run(self, text):
        return "neutral"
```

Use:

```python
plugin_class = Plugin.registry["ticket"]
plugin = plugin_class()

print(plugin.run("Cannot log in"))
```

`__init_subclass__()` is often a simpler alternative to a metaclass for subclass registration.

# 6. Pythonic design patterns

Design patterns are reusable solutions to recurring design problems. Python often implements them more simply than heavily object-oriented languages.

## Strategy pattern

Select an algorithm at runtime.

```python
class Evaluator:
    def __init__(self, strategy):
        self.strategy = strategy

    def evaluate(self, predictions, labels):
        return self.strategy.evaluate(
            predictions,
            labels,
        )
```

Strategies:

```python
class Accuracy:
    def evaluate(self, predictions, labels):
        correct = sum(
            prediction == label
            for prediction, label in zip(
                predictions,
                labels,
            )
        )

        return correct / len(labels)
```

```python
class ExactMatches:
    def evaluate(self, predictions, labels):
        return sum(
            prediction == label
            for prediction, label in zip(
                predictions,
                labels,
            )
        )
```

Use:

```python
evaluator = Evaluator(Accuracy())

score = evaluator.evaluate(
    [1, 0, 1],
    [1, 0, 0],
)
```

A function can also be a strategy:

```python
def accuracy(predictions, labels):
    ...
```

Python does not require a strategy class when a callable is enough.

## Adapter pattern

Make one interface look like another.

```python
class LegacyModel:
    def predict_text(self, text):
        return f"Legacy prediction: {text}"
```

```python
class ModelAdapter:
    def __init__(self, legacy_model):
        self._legacy_model = legacy_model

    def predict(self, text):
        return self._legacy_model.predict_text(text)
```

Now the rest of the system uses:

```python
model.predict(text)
```

even though the original API used:

```python
predict_text(text)
```

Adapters are useful for:

- Legacy systems.
- Third-party SDKs.
- Swapping cloud providers.
- Normalizing database drivers.
- Integrating older internal APIs.

## Factory pattern

A factory creates an object without exposing all construction details.

```python
class LocalProvider:
    def generate(self, prompt):
        return f"Local: {prompt}"


class CloudProvider:
    def generate(self, prompt):
        return f"Cloud: {prompt}"
```

```python
def create_provider(name):
    providers = {
        "local": LocalProvider,
        "cloud": CloudProvider,
    }

    try:
        provider_class = providers[name]
    except KeyError as error:
        raise ValueError(
            f"Unknown provider: {name}"
        ) from error

    return provider_class()
```

Use:

```python
provider = create_provider("local")
```

For simple cases, a dictionary factory is often clearer than a factory class.

## Observer pattern

Objects subscribe to events.

```python
class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name, listener):
        self._listeners.setdefault(
            event_name,
            [],
        ).append(listener)

    def publish(self, event_name, payload):
        for listener in self._listeners.get(
            event_name,
            [],
        ):
            listener(payload)
```

Use:

```python
def log_ticket(payload):
    print(f"Log: {payload}")


def notify_agent(payload):
    print(f"Agent notified: {payload}")
```

```python
bus = EventBus()

bus.subscribe("ticket.created", log_ticket)
bus.subscribe("ticket.created", notify_agent)

bus.publish(
    "ticket.created",
    {"id": "T-001"},
)
```

Output:

```text
Log: {'id': 'T-001'}
Agent notified: {'id': 'T-001'}
```

For larger systems, use queues or dedicated event infrastructure instead of an in-memory event bus.

## Context manager pattern

Context managers encapsulate resource lifecycles:

```python
with database.transaction():
    save_ticket()
```

This is the Pythonic form of setup/cleanup logic.

## Decorator pattern

Decorators add cross-cutting behavior:

```python
@measure_time
@log_calls
def classify_ticket(text):
    ...
```

Use them for:

- Logging.
- Timing.
- Authorization.
- Caching.
- Retries.
- Registration.
- Validation.

# 7. Library-level design

A library should have:

- A small public API.
- Stable interfaces.
- Clear exceptions.
- Good documentation.
- Type hints.
- Tests.
- No unwanted side effects at import time.
- Configurable logging.
- Minimal global state.

## Public API

In `trustdesk/__init__.py`:

```python
from .models import Ticket
from .services import TicketService

__all__ = [
    "Ticket",
    "TicketService",
]
```

Users write:

```python
from trustdesk import Ticket
```

rather than depending on internal module paths.

## Do not execute work at import time

Avoid:

```python
# module.py
model = load_large_model()
connect_to_database()
```

Importing the module now triggers expensive external behavior.

Prefer:

```python
def create_model():
    return load_large_model()
```

or an explicit factory:

```python
model = create_model()
```

## Use dependency injection

```python
class TicketService:
    def __init__(
        self,
        repository,
        classifier,
    ):
        self._repository = repository
        self._classifier = classifier
```

This makes the library:

- Testable.
- Configurable.
- Independent of a specific database or model.
- Easier to reuse.

## Raise meaningful exceptions

```python
class TicketError(Exception):
    """Base ticket-related error."""


class TicketNotFoundError(TicketError):
    """Requested ticket does not exist."""
```

Use:

```python
raise TicketNotFoundError(
    f"Ticket {ticket_id} was not found."
)
```

Users can catch a stable library-specific exception instead of relying on implementation details.

## Keep imports intentional

Avoid circular imports:

```text
module A imports B
module B imports A
```

Move shared protocols or data types into a lower-level module:

```text
interfaces/
models/
```

or import locally only when the dependency is genuinely optional.

# 8. Advanced standard-library modules

You have already studied many important modules. These are worth adding to your toolkit.

## `pathlib`

Object-oriented file paths:

```python
from pathlib import Path


path = Path("data") / "tickets.json"

if path.exists():
    text = path.read_text(
        encoding="utf-8"
    )
```

Prefer it over manually joining strings:

```python
"data/" + filename
```

## `dataclasses`

Structured data with generated methods:

```python
from dataclasses import dataclass


@dataclass
class Ticket:
    ticket_id: str
    title: str
```

## `enum`

Named constants:

```python
from enum import Enum


class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
```

Use:

```python
priority = Priority.HIGH

print(priority.value)
```

Enums avoid scattered strings and typos.

## `contextlib`

Context manager utilities:

```python
from contextlib import suppress


with suppress(FileNotFoundError):
    Path("cache.txt").unlink()
```

Other useful tools:

```python
contextmanager
asynccontextmanager
closing
ExitStack
nullcontext
redirect_stdout
redirect_stderr
```

## `functools`

Function tools:

```python
partial
cache
lru_cache
wraps
singledispatch
total_ordering
cached_property
```

## `operator`

Functions corresponding to operators:

```python
import operator


operator.add(2, 3)
operator.itemgetter("priority")
operator.attrgetter("name")
```

Example:

```python
from operator import itemgetter


tickets = [
    {"id": "T-001", "priority": 2},
    {"id": "T-002", "priority": 1},
]

sorted_tickets = sorted(
    tickets,
    key=itemgetter("priority"),
)
```

## `itertools`

Lazy iteration tools:

```python
chain
islice
groupby
product
accumulate
```

## `collections`

Specialized data structures:

```python
Counter
defaultdict
deque
ChainMap
```

## `enum`

Useful for statuses, modes, and categories:

```python
from enum import StrEnum


class Status(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
```

If targeting a Python version without `StrEnum`, use:

```python
class Status(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
```

## `graphlib`

Topological sorting:

```python
from graphlib import TopologicalSorter


dependencies = {
    "deploy": {"test"},
    "test": {"build"},
    "build": set(),
}

order = TopologicalSorter(
    dependencies
).static_order()

print(list(order))
```

Output:

```python
['build', 'test', 'deploy']
```

Useful for:

- Task dependencies.
- Build pipelines.
- Agent workflow ordering.
- Data pipeline stages.

## `secrets`

Secure random values:

```python
import secrets


token = secrets.token_urlsafe(32)
```

Use for tokens, not:

```python
random
```

The `random` module is not designed for security-sensitive tokens.

## `statistics`

Basic statistics:

```python
from statistics import mean, median


scores = [0.8, 0.9, 0.95]

print(mean(scores))
print(median(scores))
```

## `decimal`

Exact decimal arithmetic:

```python
from decimal import Decimal


price = Decimal("19.99")
tax = Decimal("0.18")

total = price * (1 + tax)
```

Use it for financial values where binary floating-point behavior is inappropriate.

## `sqlite3`

Built-in relational database:

```python
import sqlite3


with sqlite3.connect("tickets.db") as connection:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL
        )
        """
    )
```

## `secrets`, `hashlib`, and `hmac`

Useful security primitives:

```python
import hashlib


digest = hashlib.sha256(
    b"data"
).hexdigest()
```

Do not use raw SHA-256 for password storage. Use a password-hashing algorithm designed for passwords.

# 9. Advanced attribute patterns

## `__getattr__`

Runs only when ordinary lookup fails:

```python
class Config:
    def __init__(self, values):
        self._values = values

    def __getattr__(self, name):
        try:
            return self._values[name]
        except KeyError as error:
            raise AttributeError(
                f"Unknown setting: {name}"
            ) from error
```

```python
config = Config({
    "model": "local",
})

print(config.model)
```

## `__getattribute__`

Runs for every attribute access:

```python
class Traced:
    def __getattribute__(self, name):
        print(f"Reading {name}")

        return super().__getattribute__(name)
```

Use carefully because this can easily cause infinite recursion.

## `__setattr__`

Controls assignment:

```python
class User:
    def __setattr__(self, name, value):
        if name == "age" and value < 0:
            raise ValueError(
                "Age cannot be negative."
            )

        super().__setattr__(name, value)
```

For ordinary validation, properties are usually clearer.

## `__dir__`

Customize what `dir(obj)` displays:

```python
class DynamicAPI:
    def __dir__(self):
        return ["search", "summarize"]
```

This can improve discoverability for dynamic proxy objects, but use it only when the displayed interface is intentional.

# 10. Proxies and delegation

A proxy forwards operations to another object.

```python
class LoggingProxy:
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        attribute = getattr(self._target, name)

        if callable(attribute):
            def wrapper(*args, **kwargs):
                print(f"Calling {name}")
                return attribute(
                    *args,
                    **kwargs,
                )

            return wrapper

        return attribute
```

Use:

```python
class Calculator:
    def add(self, a, b):
        return a + b


calculator = LoggingProxy(Calculator())

print(calculator.add(2, 3))
```

Output:

```text
Calling add
5
```

This pattern is useful for:

- Logging.
- Metrics.
- Access control.
- Retries.
- Remote objects.
- Lazy loading.
- API clients.

It can confuse static type checkers, so use protocols or explicit wrapper methods when possible.

# 11. Descriptors and framework fields

Frameworks often use descriptors to turn class declarations into managed fields.

```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return getattr(
            instance,
            self.private_name,
            None,
        )

    def __set__(self, instance, value):
        print(
            f"Setting {self.name}={value!r}"
        )

        setattr(
            instance,
            self.private_name,
            value,
        )
```

Use:

```python
class Model:
    name = Field()
    status = Field()
```

```python
model = Model()

model.name = "Ticket classifier"
print(model.name)
```

Output:

```text
Setting name='Ticket classifier'
Ticket classifier
```

This is the kind of mechanism behind:

- ORM fields.
- Validation models.
- Lazy attributes.
- Configuration systems.
- Dependency injection.
- Observable properties.

# 12. Metaprogramming safety rules

Use metaprogramming carefully.

## Prefer explicit interfaces

Better:

```python
class Tool(Protocol):
    def run(self, text: str) -> str:
        ...
```

than a system that discovers arbitrary methods through strings without documentation.

## Validate dynamic names

```python
allowed = {
    "search",
    "summarize",
}

if tool_name not in allowed:
    raise ValueError("Unknown tool.")
```

## Avoid executing arbitrary code

Be cautious with:

```python
eval()
exec()
```

Never pass untrusted user input to them.

Also be careful with:

```python
pickle.load()
```

dynamic imports, shell commands, and dynamically generated code.

## Keep generated behavior inspectable

Framework magic should have:

- Clear documentation.
- Helpful errors.
- Stable public interfaces.
- Tests.
- Debugging hooks.
- Good logging.

# 13. Complete plugin example

```python
from dataclasses import dataclass
from typing import Protocol
```

Plugin contract:

```python
class Plugin(Protocol):
    name: str

    def run(self, text: str) -> str:
        ...
```

Plugin registry:

```python
PLUGIN_REGISTRY: dict[str, type[Plugin]] = {}
```

Registration decorator:

```python
def register_plugin(
    name: str,
):
    def decorator(
        plugin_class: type[Plugin],
    ) -> type[Plugin]:
        if name in PLUGIN_REGISTRY:
            raise ValueError(
                f"Plugin already registered: {name}"
            )

        PLUGIN_REGISTRY[name] = plugin_class

        return plugin_class

    return decorator
```

Implementations:

```python
@register_plugin("sentiment")
class SentimentPlugin:
    name = "sentiment"

    def run(self, text: str) -> str:
        if "good" in text.lower():
            return "positive"

        return "neutral"
```

```python
@register_plugin("category")
class CategoryPlugin:
    name = "category"

    def run(self, text: str) -> str:
        if "payment" in text.lower():
            return "billing"

        return "general"
```

Framework runner:

```python
@dataclass
class PluginRunner:
    registry: dict[str, type[Plugin]]

    def run(
        self,
        name: str,
        text: str,
    ) -> str:
        plugin_class = self.registry.get(name)

        if plugin_class is None:
            raise ValueError(
                f"Unknown plugin: {name}"
            )

        plugin = plugin_class()

        return plugin.run(text)
```

Use:

```python
runner = PluginRunner(
    PLUGIN_REGISTRY
)

print(
    runner.run(
        "category",
        "My payment failed.",
    )
)
```

Output:

```text
billing
```

This example combines:

```text
Protocol       → plugin contract
decorator      → automatic registration
registry       → dynamic lookup
dataclass      → runner configuration
polymorphism   → different plugins share run()
```

# 14. Practice exercises

## Exercise 1: Introspection

Write a function that accepts any object and prints:

```text
class name
available public methods
instance attributes
```

Use:

```python
type()
dir()
vars()
inspect.getmembers()
```

## Exercise 2: Dynamic dispatcher

Create a command registry with:

```text
add
list
delete
```

Register each command with a decorator and execute it by name.

## Exercise 3: Plugin loader

Write a function using:

```python
importlib.import_module()
```

to load a plugin class from a module path and class name.

## Exercise 4: Descriptor

Create a descriptor that validates all assigned values are non-empty strings.

## Exercise 5: Strategy pattern

Create an evaluator that accepts either:

```text
AccuracyStrategy
F1Strategy
```

through composition.

## Exercise 6: `__init_subclass__`

Create a base `Command` class that automatically registers subclasses by a class attribute called:

```python
command_name
```

# 15. Final mental model

```text
Introspection
    → inspect live objects and signatures

getattr/setattr
    → access attributes dynamically

inspect
    → inspect signatures, members, source, and stack

importlib
    → load modules programmatically

registries
    → map names to handlers or plugins

decorators
    → transform or register functions/classes

descriptors
    → control attribute access

__init_subclass__
    → customize subclass creation

metaclasses
    → customize class creation itself
```

Use this progression:

```text
normal function/class
    ↓
dispatch dictionary
    ↓
decorator registry
    ↓
__init_subclass__
    ↓
descriptor
    ↓
metaclass
```

Only move downward when the simpler approach no longer expresses the design clearly.

For your AI projects:

```text
inspect.signature → generate tool schemas
getattr            → dynamic plugin capabilities
Protocol           → stable provider interfaces
decorator registry → agent tool registration
importlib          → controlled plugin loading
dataclass          → configuration and result models
descriptor         → validated framework fields
__init_subclass__  → model/tool auto-registration
```

The main rule is:

> Metaprogramming should reduce repetition and create a clearer extension point—not make ordinary code mysterious.

Use introspection and dynamic dispatch frequently when appropriate. Use descriptors and `__init_subclass__()` when building reusable frameworks. Reserve metaclasses for genuine class-creation problems that cannot be solved cleanly with simpler tools. [docs.python](https://docs.python.org/3/library/inspect.html)
