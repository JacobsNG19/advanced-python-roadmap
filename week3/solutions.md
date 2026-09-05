# Advanced Object-Oriented Programming & Python's Object Model — Solutions

These solutions correspond to:

```text
Advanced Object-Oriented Programming & Python's Object Model - Exercises.md
```

---

## Exercise 1 — Human-readable and developer representations

```python
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return (
            f"{self.title} — "
            f"{self.author} ({self.year})"
        )

    def __repr__(self):
        return (
            f"Book(" 
            f"title={self.title!r}, "
            f"author={self.author!r}, "
            f"year={self.year!r}"
            f")"
        )
```

`__str__` is human-friendly. `__repr__` is intended for developers and debugging.

---

## Exercise 2 — Equality by identifier

```python
class Ticket:
    def __init__(self, ticket_id, title):
        self.ticket_id = ticket_id
        self.title = title

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return NotImplemented

        return self.ticket_id == other.ticket_id
```

Returning `NotImplemented` allows Python to apply normal comparison behavior for unrelated types.

---

## Exercise 3 — Hashable ticket keys

```python
class TicketKey:
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id

    def __eq__(self, other):
        if not isinstance(other, TicketKey):
            return NotImplemented

        return self.ticket_id == other.ticket_id

    def __hash__(self):
        return hash(self.ticket_id)

    def __repr__(self):
        return f"TicketKey({self.ticket_id!r})"
```

The object is safe to hash only because its identity field should not change after insertion into a set or dictionary.

---

## Exercise 4 — Vector operations

```python
import math


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented

        return Vector2D(
            self.x + other.x,
            self.y + other.y,
        )

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __abs__(self):
        return math.sqrt(
            self.x ** 2 + self.y ** 2
        )

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"
```

---

## Exercise 5 — Collection object

```python
class TicketCollection:
    def __init__(self, ticket_ids=()):
        self._ticket_ids = list(ticket_ids)

    def __len__(self):
        return len(self._ticket_ids)

    def __getitem__(self, index):
        return self._ticket_ids[index]

    def __iter__(self):
        return iter(self._ticket_ids)

    def __contains__(self, value):
        return value in self._ticket_ids
```

The collection returns a new iterator each time, so it can be traversed repeatedly.

---

## Exercise 6 — Callable classifier

```python
class KeywordClassifier:
    def __call__(self, text):
        normalized = text.lower()

        if "payment" in normalized:
            return "billing"

        if "password" in normalized:
            return "account_access"

        return "general"
```

`__call__` makes an instance callable like a function.

---

## Exercise 7 — Managed resource

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

Returning `False` allows exceptions inside the block to propagate.

---

## Exercise 8 — Validated temperature

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(
                "Temperature must be numeric."
            )

        if value < -273.15:
            raise ValueError(
                "Temperature cannot be below absolute zero."
            )

        self._celsius = value
```

The public attribute is controlled by getter and setter methods.

---

## Exercise 9 — Read-only balance

```python
class BankAccount:
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError(
                "Balance cannot be negative."
            )

        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(
                "Deposit must be positive."
            )

        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError(
                "Withdrawal must be positive."
            )

        if amount > self._balance:
            raise ValueError(
                "Insufficient funds."
            )

        self._balance -= amount
```

Because there is no `balance.setter`, direct assignment to `account.balance` fails.

---

## Exercise 10 — Reusable validated field

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return getattr(
            instance,
            self.private_name,
        )

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"{self.public_name} must be numeric."
            )

        if value <= 0:
            raise ValueError(
                f"{self.public_name} must be positive."
            )

        setattr(
            instance,
            self.private_name,
            value,
        )


class Subscription:
    monthly_price = PositiveNumber()
    months = PositiveNumber()

    def __init__(self, monthly_price, months):
        self.monthly_price = monthly_price
        self.months = months

    @property
    def total(self):
        return self.monthly_price * self.months
```

The descriptor reuses the same validation behavior for multiple attributes.

---

## Exercise 11 — Animal hierarchy

```python
class Animal:
    def speak(self):
        raise NotImplementedError


class Dog(Animal):
    def speak(self):
        return "Woof!"


class Cat(Animal):
    def speak(self):
        return "Meow!"


animals = [Dog(), Cat()]

assert [animal.speak() for animal in animals] == [
    "Woof!",
    "Meow!",
]
```

The common method name enables polymorphic use.

---

## Exercise 12 — Parent initialization

```python
class User:
    def __init__(self, username):
        self.username = username

    def describe(self):
        return f"User: {self.username}"


class AdminUser(User):
    def __init__(self, username, permissions):
        super().__init__(username)
        self.permissions = permissions

    def describe(self):
        base = super().describe()

        return (
            f"{base}; "
            f"permissions={self.permissions}"
        )
```

`super()` reuses both parent initialization and parent behavior.

---

## Exercise 13 — MRO experiment

```python
class A:
    def show(self):
        return "A"


class B(A):
    def show(self):
        return "B"


class C(A):
    def show(self):
        return "C"


class D(B, C):
    pass


assert D().show() == "B"
assert D.mro() == [D, B, C, A, object]
```

Python follows the class method-resolution order, not simply the first textual parent in every situation.

---

## Exercise 14 — Cooperative mixins

```python
class BaseService:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LoggingMixin:
    def __init__(self, **kwargs):
        self.logging_ready = True
        super().__init__(**kwargs)


class ValidationMixin:
    def __init__(self, **kwargs):
        self.validation_ready = True
        super().__init__(**kwargs)


class Service(
    LoggingMixin,
    ValidationMixin,
    BaseService,
):
    def __init__(self):
        super().__init__()
```

Each class calls `super()`, allowing the next class in the MRO to participate.

---

## Exercise 15 — Abstract repository

```python
from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def save(self, item_id, item):
        pass

    @abstractmethod
    def get_by_id(self, item_id):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._items = {}

    def save(self, item_id, item):
        self._items[item_id] = item

    def get_by_id(self, item_id):
        return self._items.get(item_id)
```

`Repository()` cannot be instantiated because it has abstract methods.

---

## Exercise 16 — Structural provider interface

```python
from typing import Protocol


class ModelProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class LocalProvider:
    def generate(self, prompt: str) -> str:
        return f"Local response: {prompt}"


class CloudProvider:
    def generate(self, prompt: str) -> str:
        return f"Cloud response: {prompt}"


class Assistant:
    def __init__(self, provider: ModelProvider):
        self._provider = provider

    def answer(self, question: str) -> str:
        return self._provider.generate(question)
```

Both implementations satisfy the protocol structurally without inheriting from it.

---

## Exercise 17 — Dataclass with validation

```python
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float

    def __post_init__(self):
        self.name = self.name.strip()

        if not self.name:
            raise ValueError(
                "Name cannot be empty."
            )

        if self.price < 0:
            raise ValueError(
                "Price cannot be negative."
            )
```

The dataclass supplies useful generated initialization and representation methods.

---

## Exercise 18 — Independent mutable fields

```python
from dataclasses import dataclass, field


@dataclass
class Project:
    name: str
    tasks: list[str] = field(
        default_factory=list
    )
```

`default_factory=list` creates a new list for each instance.

---

## Exercise 19 — Immutable value object

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int
```

`frozen=True` prevents normal reassignment and gives value-like equality. For these immutable fields, instances can be used as set members.

---

## Exercise 20 — Dataclass serialization

```python
from dataclasses import asdict, dataclass
import json


@dataclass
class ExperimentResult:
    model_name: str
    accuracy: float
    samples: int


result = ExperimentResult(
    "classifier-v1",
    0.94,
    1000,
)

payload = asdict(result)
encoded = json.dumps(payload)
decoded = json.loads(encoded)
restored = ExperimentResult(**decoded)

assert restored == result
```

`asdict()` creates JSON-compatible dictionary data for this dataclass.

---

## Exercise 21 — Automatic subclass registry

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

        if plugin_name in Plugin.registry:
            raise ValueError(
                f"Duplicate plugin: {plugin_name}"
            )

        Plugin.registry[plugin_name] = cls


class SearchPlugin(
    Plugin,
    plugin_name="search",
):
    def run(self, text):
        return f"Searching: {text}"
```

`__init_subclass__()` runs when a subclass is created and is often simpler than a metaclass.

---

## Exercise 22 — Class registration system

```python
PLUGIN_REGISTRY = {}


def register_plugin(name):
    def decorator(cls):
        if name in PLUGIN_REGISTRY:
            raise ValueError(
                f"Duplicate plugin: {name}"
            )

        PLUGIN_REGISTRY[name] = cls
        return cls

    return decorator


@register_plugin("search")
class SearchPlugin:
    def run(self, text):
        return f"Searching: {text}"


plugin = PLUGIN_REGISTRY["search"]()
assert plugin.run("Python") == "Searching: Python"
```

A registry decorator is often preferable to a metaclass when registration is the only required behavior.

---

## Exercise 23 — Metaclass validation

```python
class ToolMeta(type):
    def __new__(metaclass, name, bases, namespace):
        if name != "BaseTool" and "run" not in namespace:
            raise TypeError(
                f"{name} must define run()."
            )

        return super().__new__(
            metaclass,
            name,
            bases,
            namespace,
        )


class BaseTool(metaclass=ToolMeta):
    pass


class SearchTool(BaseTool):
    def run(self, text):
        return f"Search: {text}"
```

A broken subclass is rejected while its class is being created:

```python
# class BrokenTool(BaseTool):
#     pass
```

For most application code, prefer a protocol, ABC, decorator, or `__init_subclass__()` first.

---

## Exercise 24 — Dynamic proxy

```python
class LoggingProxy:
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        attribute = getattr(self._target, name)

        if callable(attribute):
            def wrapper(*args, **kwargs):
                print(f"Calling {name}")
                return attribute(*args, **kwargs)

            return wrapper

        return attribute
```

Example:

```python
class Calculator:
    def add(self, first, second):
        return first + second


calculator = LoggingProxy(Calculator())
assert calculator.add(2, 3) == 5
```

`__getattr__()` runs when normal attribute lookup fails on the proxy.

---

## Exercise 25 — Final typed ticket system

```python
from dataclasses import dataclass
from typing import Literal, Protocol


Status = Literal["open", "closed"]


class Classifier(Protocol):
    def classify(self, text: str) -> str:
        ...


@dataclass
class Ticket:
    ticket_id: str
    title: str
    _status: Status = "open"

    @property
    def status(self) -> Status:
        return self._status

    def close(self) -> None:
        self._status = "closed"

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return NotImplemented

        return self.ticket_id == other.ticket_id


class KeywordClassifier:
    def classify(self, text: str) -> str:
        normalized = text.lower()

        if "payment" in normalized:
            return "billing"

        if "password" in normalized:
            return "account_access"

        return "general"


class TicketService:
    def __init__(self, classifier: Classifier):
        self._classifier = classifier

    def classify(self, ticket: Ticket) -> str:
        return self._classifier.classify(
            ticket.title
        )


classifier = KeywordClassifier()
service = TicketService(classifier)
ticket = Ticket("T-001", "Payment failed")

assert service.classify(ticket) == "billing"
assert ticket.status == "open"

ticket.close()
assert ticket.status == "closed"
```

This solution combines protocols, composition, a dataclass, a property, a literal status type, equality, and polymorphism.

---

# Review checklist

You should now understand:

- How dunder methods connect objects to Python syntax.
- The difference between `__str__` and `__repr__`.
- Equality and hash compatibility.
- Returning `NotImplemented`.
- Collection, callable, and context-manager protocols.
- Properties and descriptors.
- Inheritance, MRO, and `super()`.
- Cooperative mixins.
- ABCs versus protocols.
- Dataclass defaults, validation, freezing, and serialization.
- Class decorators and subclass registries.
- When `__init_subclass__()` is preferable to a metaclass.
- How metaclasses validate class creation.
- Why composition is often more flexible than deep inheritance.
