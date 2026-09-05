# Advanced Object-Oriented Programming & Python's Object Model — Complete Exercises

This workbook covers:

- Dunder and magic methods.
- Equality, hashing, and operator overloading.
- Collection and callable protocols.
- Properties and descriptors.
- Inheritance, MRO, `super()`, mixins, and multiple inheritance.
- Abstract Base Classes.
- Protocol-based design.
- Dataclasses and data modeling.
- `__init_subclass__()`.
- Metaclasses.

---

## Exercise 1 — `__repr__` and `__str__`

Create a `Book` class with `title`, `author`, and `year`.

Expected:

```python
print(book)
# Python for AI Engineers — Toussaint Jacobs (2026)
```

### Solution

```python
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        return (
            f"Book(" 
            f"title={self.title!r}, "
            f"author={self.author!r}, "
            f"year={self.year!r}"
            f")"
        )

    def __str__(self):
        return (
            f"{self.title} — "
            f"{self.author} ({self.year})"
        )


book = Book(
    "Python for AI Engineers",
    "Toussaint Jacobs",
    2026,
)

assert str(book) == (
    "Python for AI Engineers — "
    "Toussaint Jacobs (2026)"
)
```

---

## Exercise 2 — Equality by identifier

Create a `Ticket` class where two tickets are equal when their IDs are equal.

Return `NotImplemented` for unsupported comparisons.

### Solution

```python
class Ticket:
    def __init__(self, ticket_id, title):
        self.ticket_id = ticket_id
        self.title = title

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return NotImplemented

        return self.ticket_id == other.ticket_id


first = Ticket("T-001", "Cannot log in")
second = Ticket("T-001", "Different title")
third = Ticket("T-002", "Cannot log in")

assert first == second
assert first != third
assert (first == "T-001") is False
```

---

## Exercise 3 — Hashable immutable value object

Create a hashable `TicketKey` class. Equal keys must have equal hashes.

### Solution

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


first = TicketKey("T-001")
second = TicketKey("T-001")

assert first == second
assert hash(first) == hash(second)
assert len({first, second}) == 1
```

Do not use mutable fields in `__hash__` if they can change after insertion into a set or dictionary.

---

## Exercise 4 — Vector arithmetic

Create a `Vector2D` class supporting:

```python
v1 + v2
-v1
abs(v1)
```

### Solution

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

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"


first = Vector2D(1, 2)
second = Vector2D(3, 4)

assert first + second == Vector2D(4, 6)
assert -first == Vector2D(-1, -2)
assert abs(Vector2D(3, 4)) == 5
```

For the equality assertion to work, add this method:

```python
    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented

        return self.x == other.x and self.y == other.y
```

---

## Exercise 5 — Custom collection

Create `TicketCollection` supporting:

```python
len(collection)
collection[index]
for ticket in collection
value in collection
```

### Solution

```python
class TicketCollection:
    def __init__(self, tickets=()):
        self._tickets = list(tickets)

    def __len__(self):
        return len(self._tickets)

    def __getitem__(self, index):
        return self._tickets[index]

    def __iter__(self):
        return iter(self._tickets)

    def __contains__(self, value):
        return value in self._tickets

    def __repr__(self):
        return f"TicketCollection({self._tickets!r})"


collection = TicketCollection([
    "T-001",
    "T-002",
])

assert len(collection) == 2
assert collection[0] == "T-001"
assert list(collection) == ["T-001", "T-002"]
assert "T-002" in collection
```

---

## Exercise 6 — Callable object

Create `KeywordClassifier` so that its instances can be called like functions.

### Solution

```python
class KeywordClassifier:
    def __call__(self, text):
        normalized = text.lower()

        if "payment" in normalized:
            return "billing"

        if "password" in normalized:
            return "account_access"

        return "general"


classifier = KeywordClassifier()

assert classifier("Payment failed") == "billing"
assert classifier("Forgot password") == "account_access"
assert classifier("Feature request") == "general"
```

---

## Exercise 7 — Context-manager object

Create a context manager that opens and closes a fake resource.

### Solution

```python
class Session:
    def __enter__(self):
        self.opened = True
        return self

    def query(self, sql):
        if not self.opened:
            raise RuntimeError("Session is closed.")

        return f"Result for: {sql}"

    def __exit__(self, exc_type, exc_value, traceback):
        self.opened = False
        return False


with Session() as session:
    assert session.query(
        "SELECT * FROM tickets"
    ) == "Result for: SELECT * FROM tickets"
```

---

## Exercise 8 — Validated property

Create a `Temperature` class with a Celsius property that rejects values below absolute zero.

### Solution

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
                "Below absolute zero."
            )

        self._celsius = value


temperature = Temperature(25)
assert temperature.celsius == 25

temperature.celsius = 30
assert temperature.celsius == 30
```

---

## Exercise 9 — Read-only property

Create a `BankAccount` with a read-only `balance`. Balance may change only through `deposit()` and `withdraw()`.

### Solution

```python
class BankAccount:
    def __init__(self, initial_balance=0):
        if initial_balance < 0:
            raise ValueError(
                "Balance cannot be negative."
            )

        self._balance = initial_balance

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


account = BankAccount(100)
account.deposit(50)
account.withdraw(20)

assert account.balance == 130
```

---

## Exercise 10 — Reusable descriptor

Create a `PositiveNumber` descriptor that can be reused for several attributes.

### Solution

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


subscription = Subscription(20, 12)
assert subscription.total == 240
```

---

## Exercise 11 — Simple inheritance

Create `Animal`, `Dog`, and `Cat`. Both child classes should override `speak()`.

### Solution

```python
class Animal:
    def speak(self):
        return "Some animal sound."


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

---

## Exercise 12 — Inheritance and `super()`

Create a base `User` and child `AdminUser`. Reuse parent initialization and description.

### Solution

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


admin = AdminUser(
    "toussaint",
    ["read", "write"],
)

assert admin.username == "toussaint"
assert "permissions" in admin.describe()
```

---

## Exercise 13 — MRO inspection

Create classes `A`, `B(A)`, `C(A)`, and `D(B, C)`. Inspect the MRO and determine which `show()` executes.

### Solution

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

---

## Exercise 14 — Cooperative mixins

Create two mixins that cooperate through `super()`.

### Solution

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


service = Service()
assert service.logging_ready is True
assert service.validation_ready is True
```

---

## Exercise 15 — Abstract Base Class

Create an abstract `Repository` with `save()` and `get_by_id()`. Implement `InMemoryRepository`.

### Solution

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


repository = InMemoryRepository()
repository.save("T-001", {"title": "Cannot log in"})

assert repository.get_by_id("T-001") == {
    "title": "Cannot log in"
}
```

---

## Exercise 16 — Protocol-based composition

Define a `Notifier` protocol and create email and SMS implementations. Build a service that depends only on the protocol.

### Solution

```python
from typing import Protocol


class Notifier(Protocol):
    def send(self, message: str) -> str:
        ...


class EmailNotifier:
    def send(self, message: str) -> str:
        return f"Email: {message}"


class SMSNotifier:
    def send(self, message: str) -> str:
        return f"SMS: {message}"


class AlertService:
    def __init__(self, notifier: Notifier):
        self._notifier = notifier

    def alert(self, message: str) -> str:
        return self._notifier.send(message)


assert AlertService(
    EmailNotifier()
).alert("Ready") == "Email: Ready"

assert AlertService(
    SMSNotifier()
).alert("Ready") == "SMS: Ready"
```

---

## Exercise 17 — Basic dataclass

Create a `Ticket` dataclass with `id`, `title`, and `priority`.

### Solution

```python
from dataclasses import dataclass


@dataclass
class Ticket:
    ticket_id: str
    title: str
    priority: str


ticket = Ticket(
    "T-001",
    "Cannot log in",
    "high",
)

assert ticket.ticket_id == "T-001"
assert "Cannot log in" in repr(ticket)
```

---

## Exercise 18 — Dataclass validation

Validate a dataclass in `__post_init__()`.

### Solution

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


product = Product("  API Plan  ", 20)
assert product.name == "API Plan"
```

---

## Exercise 19 — Dataclass mutable defaults

Create a `Project` dataclass with an independent task list for every instance.

### Solution

```python
from dataclasses import dataclass, field


@dataclass
class Project:
    name: str
    tasks: list[str] = field(
        default_factory=list
    )


first = Project("TrustDesk")
second = Project("Burvex")

first.tasks.append("Build MVP")

assert first.tasks == ["Build MVP"]
assert second.tasks == []
```

---

## Exercise 20 — Frozen dataclass

Create an immutable `Point` dataclass that can be placed in a set.

### Solution

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


first = Point(1, 2)
second = Point(1, 2)

assert first == second
assert len({first, second}) == 1
```

---

## Exercise 21 — Dataclass serialization

Convert a dataclass into JSON-compatible data.

### Solution

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
json_text = json.dumps(payload)

restored = ExperimentResult(
    **json.loads(json_text)
)

assert restored == result
```

---

## Exercise 22 — `__init_subclass__()` registry

Create a base `Plugin` class that automatically registers subclasses using a `plugin_name` keyword.

### Solution

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


class TicketPlugin(
    Plugin,
    plugin_name="ticket",
):
    def run(self, text):
        return "general"


plugin = Plugin.registry["ticket"]()
assert plugin.run("Question") == "general"
```

---

## Exercise 23 — Class decorator registry

Register plugin classes with a decorator.

### Solution

```python
PLUGIN_REGISTRY = {}


def register_plugin(name):
    def decorator(cls):
        if name in PLUGIN_REGISTRY:
            raise ValueError(
                f"Already registered: {name}"
            )

        PLUGIN_REGISTRY[name] = cls
        return cls

    return decorator


@register_plugin("sentiment")
class SentimentPlugin:
    def run(self, text):
        return "positive"


plugin = PLUGIN_REGISTRY["sentiment"]()
assert plugin.run("good") == "positive"
```

---

## Exercise 24 — Metaclass validation

Create a metaclass that requires every subclass of `BaseTool` to define a `run()` method.

### Solution

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
    def run(self, query):
        return f"Searching: {query}"


assert SearchTool().run("Python") == "Searching: Python"
```

The following would fail during class creation:

```python
# class BrokenTool(BaseTool):
#     pass
```

In real application code, first consider a protocol, ABC, decorator, or `__init_subclass__()` before a metaclass.

---

## Exercise 25 — Final object-model project

Build a typed ticket system using:

- A dataclass for the ticket.
- A protocol for classification.
- Composition in the service.
- A property for controlled status.
- Equality by ticket ID.
- A registry for classifier implementations.

### Complete solution

```python
from dataclasses import dataclass
from typing import Literal, Protocol


Status = Literal[
    "open",
    "closed",
]


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

    def __repr__(self):
        return (
            f"Ticket(" 
            f"ticket_id={self.ticket_id!r}, "
            f"title={self.title!r}, "
            f"status={self.status!r}"
            f")"
        )


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
ticket = Ticket(
    "T-001",
    "Payment failed",
)

assert service.classify(ticket) == "billing"
assert ticket.status == "open"

ticket.close()

assert ticket.status == "closed"
```

---

# Suggested execution order

1. Exercises 1–7: dunder methods and object protocols.
2. Exercises 8–10: properties and descriptors.
3. Exercises 11–16: inheritance, MRO, ABCs, and protocols.
4. Exercises 17–21: dataclasses and data modeling.
5. Exercises 22–24: registration, subclass hooks, and metaclasses.
6. Exercise 25: integrated object-model project.

# Mastery checklist

You should be able to explain:

- The difference between `__repr__` and `__str__`.
- Why equal objects need compatible hashes.
- When to return `NotImplemented`.
- How operator overloading works.
- How `__getitem__`, `__iter__`, and `__contains__` make an object collection-like.
- How descriptors control attribute access.
- Why properties are descriptors.
- How MRO determines method lookup.
- Why cooperative multiple inheritance uses `super()`.
- When composition is better than inheritance.
- When to use an ABC versus a Protocol.
- How dataclasses reduce boilerplate.
- Why mutable dataclass defaults need `default_factory`.
- When `__init_subclass__()` is preferable to a metaclass.
- What metaclasses control.

# Final challenge

Design a pluggable AI support system with:

```text
Protocol for model providers
Dataclass for model responses
Descriptor for validated confidence scores
ABC for formal evaluator implementations
Composition for the support service
Class registry for plugins
A custom __repr__ for observability
```

The goal is to use Python's object model to create clear extension points—not to add metaprogramming merely for complexity.
