Python’s object model explains how classes, objects, inheritance, attributes, operators, properties, dataclasses, and metaclasses work internally. The practical order is: learn dunder methods, descriptors, inheritance and MRO, ABCs, dataclasses, then metaclasses last. Python’s data model defines these protocols, while descriptors control attribute access and dataclasses generate common class methods from annotated fields.[[docs.python](https://docs.python.org/3/reference/datamodel.html?highlight=setattr)][[docs.python](https://docs.python.org/3/howto/descriptor.html)][[docs.python](https://docs.python.org/3/library/dataclasses.html)]

# 1. Dunder methods

Dunder methods are special hooks with names such as:

```
__init__
__str__
__repr__
__eq__
__len__
__iter__
__add__
```

You usually trigger them through normal syntax:

```
str(obj)       # obj.__str__()
repr(obj)      # obj.__repr__()
len(obj)       # obj.__len__()
obj == other   # obj.__eq__(other)
obj + other    # obj.__add__(other)
```

The purpose is to let custom objects behave naturally with Python’s built-in operations.[[docs.python](https://docs.python.org/3/reference/datamodel.html?highlight=setattr)]

## `__init__`

```
class User:
    def __init__(self, username):
        self.username = username
```

```
user = User("Toussaint")
```

`__init__` initializes an already-created object. It does not technically create the object; `__new__` handles creation.

## `__repr__`

Use `__repr__` for an unambiguous developer representation:

```
class Ticket:
    def __init__(self, ticket_id, title):
        self.ticket_id = ticket_id
        self.title = title

    def __repr__(self):
        return (
            f"Ticket("
            f"ticket_id={self.ticket_id!r}, "
            f"title={self.title!r}"
            f")"
        )
```

```
ticket = Ticket(
    "T-001",
    "Cannot log in",
)

print(repr(ticket))
```

Output:

```
Ticket(ticket_id='T-001', title='Cannot log in')
```

Use `!r` when you want string values to appear with quotes and escaped characters.

## `__str__`

Use `__str__` for human-friendly output:

```
class Ticket:
    def __init__(self, ticket_id, title, priority):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority

    def __str__(self):
        return (
            f"[{self.priority.upper()}] "
            f"{self.ticket_id}: {self.title}"
        )
```

```
print(ticket)
```

If `__str__` is absent, Python falls back to `__repr__`.

---

# 2. Equality and hashing

## `__eq__`

By default, two separate objects are not equal even if their attributes match.

```
class User:
    def __init__(self, user_id):
        self.user_id = user_id
```

```
user_a = User("U-001")
user_b = User("U-001")

print(user_a == user_b)
```

Output:

```
False
```

Define logical equality:

```
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented

        return self.user_id == other.user_id
```

Now:

```
print(user_a == user_b)
```

returns:

```
True
```

Use `NotImplemented` when the other object is not a compatible type. This allows Python to apply its normal comparison rules.

## `__hash__`

Hashing is used by:

```
set
dict keys
```

If two objects compare equal:

```
a == b
```

they must have the same hash:

```
hash(a) == hash(b)
```

For an immutable value object:

```
class UserKey:
    def __init__(self, user_id):
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, UserKey):
            return NotImplemented

        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)
```

```
first = UserKey("U-001")
second = UserKey("U-001")

print(first == second)
print(len({first, second}))
```

Output:

```
True
1
```

Do not hash mutable objects based on fields that can change.

```
class MutableUser:
    def __init__(self, username):
        self.username = username

    def __hash__(self):
        return hash(self.username)
```

If `username` changes after the object enters a set, the set can become unreliable.

A safe rule:

```
Immutable value object → may implement __hash__
Mutable object          → usually leave unhashable
```

---

# 3. Operator overloading

Operator overloading means defining how your object responds to operators.

|Expression|Method|
|---|---|
|`a + b`|`__add__`|
|`a - b`|`__sub__`|
|`a * b`|`__mul__`|
|`a / b`|`__truediv__`|
|`a < b`|`__lt__`|
|`a == b`|`__eq__`|
|`-a`|`__neg__`|
|`a += b`|`__iadd__`|

## Example: vector

```
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        return Vector(
            self.x + other.x,
            self.y + other.y,
        )

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
```

```
first = Vector(1, 2)
second = Vector(3, 4)

print(first + second)
```

Output:

```
Vector(4, 6)
```

Return a new object for normal arithmetic unless mutation is explicitly expected.

## Reverse operators

For:

```
number + object
```

Python may try:

```
object.__radd__(number)
```

Example:

```
class Score:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Score):
            return Score(self.value + other.value)

        if isinstance(other, (int, float)):
            return Score(self.value + other)

        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return f"Score({self.value})"
```

```
print(10 + Score(5))
```

Output:

```
Score(15)
```

---

# 4. Collection protocols

## `__len__`

```
class TaskBoard:
    def __init__(self, tasks):
        self._tasks = list(tasks)

    def __len__(self):
        return len(self._tasks)
```

```
board = TaskBoard([
    "Design API",
    "Write tests",
])

print(len(board))
```

## `__getitem__`

```
class TaskBoard:
    def __init__(self, tasks):
        self._tasks = list(tasks)

    def __getitem__(self, index):
        return self._tasks[index]
```

```
print(board[0])
print(board[0:1])
```

## `__iter__`

```
class TaskBoard:
    def __init__(self, tasks):
        self._tasks = list(tasks)

    def __iter__(self):
        return iter(self._tasks)
```

```
for task in board:
    print(task)
```

## `__contains__`

```
class TaskBoard:
    def __contains__(self, task):
        return task in self._tasks
```

Now:

```
"Design API" in board
```

works naturally.

---

# 5. Callable and context-manager protocols

## `__call__`

```
class TextCleaner:
    def __call__(self, text):
        return text.strip().lower()
```

```
cleaner = TextCleaner()

print(cleaner("  HELLO  "))
```

Output:

```
hello
```

This is useful for:

- ML preprocessing.
- Pipeline transformations.
- Configurable callbacks.
- Agent tools.
- Strategy objects.

## `__enter__` and `__exit__`

```
class Session:
    def __enter__(self):
        print("Session opened.")
        return self

    def query(self, sql):
        return f"Running: {sql}"

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        print("Session closed.")
        return False
```

```
with Session() as session:
    print(session.query("SELECT * FROM tickets"))
```

Output:

```
Session opened.
Running: SELECT * FROM tickets
Session closed.
```

---

# 6. Properties and descriptors

A property provides controlled attribute access:

```
class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError(
                "Price cannot be negative."
            )

        self._price = value
```

Usage:

```
product = Product(100)

print(product.price)

product.price = 120
```

The public API looks like an attribute:

```
product.price
```

but Python executes getter and setter logic.

Properties are built using the descriptor protocol. Descriptors are objects that customize attribute access, storage, and deletion.[[docs.python](https://docs.python.org/3/howto/descriptor.html)]

---

# 7. Descriptor protocol

A descriptor is a class defining one or more of:

```
__get__
__set__
__delete__
```

## Reusable validator descriptor

```
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
```

Use it:

```
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

```
subscription = Subscription(20, 12)

print(subscription.total)
```

Output:

```
240
```

## How assignment works

This:

```
subscription.monthly_price = 20
```

causes Python to call approximately:

```
PositiveNumber.__set__(
    subscription,
    20,
)
```

This:

```
subscription.monthly_price
```

causes:

```
PositiveNumber.__get__(
    subscription,
    Subscription,
)
```

## Data versus non-data descriptors

A descriptor defining:

```
__set__
```

or:

```
__delete__
```

is generally a **data descriptor**.

A descriptor defining only:

```
__get__
```

is generally a **non-data descriptor**.

Data descriptors usually take priority over instance attributes during lookup.

You do not need to memorize the complete lookup algorithm yet. Know the practical fact:

```
property, methods, staticmethod, and classmethod rely on descriptor behavior.
```

---

# 8. Attribute lookup

When Python evaluates:

```
obj.attribute
```

it searches through:

1. The class’s data descriptors.
2. The instance dictionary.
3. The class and its bases.
4. `__getattr__` if normal lookup fails.

A simplified example:

```
class Example:
    value = 10

    def __init__(self):
        self.value = 20
```

```
example = Example()

print(example.value)
```

Output:

```
20
```

The instance value shadows the ordinary class attribute.

But a data descriptor, such as a property, can control access before the instance dictionary is used.

This is why properties can protect internal storage.

---

# 9. Inheritance deep dive

Inheritance creates a parent-child relationship.

```
class User:
    def describe(self):
        return "Generic user."


class AdminUser(User):
    def delete_user(self):
        return "User deleted."
```

```
admin = AdminUser()

print(admin.describe())
print(admin.delete_user())
```

The child receives the parent’s methods.

## Overriding

```
class AdminUser(User):
    def describe(self):
        return "Administrator."
```

```
print(AdminUser().describe())
```

Output:

```
Administrator.
```

## `super()`

```
class User:
    def __init__(self, username):
        self.username = username

    def describe(self):
        return f"User: {self.username}"
```

```
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

```
admin = AdminUser(
    "toussaint",
    ["read", "write"],
)

print(admin.describe())
```

Output:

```
User: toussaint; permissions=['read', 'write']
```

`super()` means:

```
Call the next implementation according to the MRO.
```

It is not merely a hardcoded direct-parent call.

---

# 10. Method Resolution Order

The **Method Resolution Order**, or MRO, determines where Python searches for methods.

```
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
```

```
print(D.mro())
print(D().show())
```

The result begins:

```
D
B
C
A
object
```

So:

```
D().show()
```

returns:

```
B
```

Inspect MRO with:

```
D.mro()
```

or:

```
D.__mro__
```

The final base class is usually:

```
object
```

because all normal Python classes ultimately inherit from it.

---

# 11. Cooperative multiple inheritance

Multiple inheritance works best when every class cooperates through `super()`.

```
class Base:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LoggingMixin:
    def __init__(self, **kwargs):
        print("Logging initialized.")
        super().__init__(**kwargs)


class ValidationMixin:
    def __init__(self, **kwargs):
        print("Validation initialized.")
        super().__init__(**kwargs)


class Service(
    LoggingMixin,
    ValidationMixin,
    Base,
):
    def __init__(self):
        super().__init__()
```

```
service = Service()
```

Output:

```
Logging initialized.
Validation initialized.
```

Each class passes control to the next class in the MRO.

## The fragile version

```
class LoggingMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ValidationMixin:
    def __init__(self, **kwargs):
        Base.__init__(self)
```

Calling `Base.__init__()` directly breaks cooperative MRO because it skips the next class in the chain.

Use:

```
super().__init__(**kwargs)
```

in cooperative multiple inheritance.

---

# 12. Multiple-inheritance pitfalls

Common problems include:

- Ambiguous method names.
- Complicated MRO.
- Parent constructors requiring incompatible arguments.
- Forgetting `super()`.
- Calling a specific parent directly.
- Deep, confusing hierarchies.
- Unexpected shared state.
- Diamond inheritance.

## Diamond pattern

```
      A
     / \
    B   C
     \ /
      D
```

Python’s MRO resolves the diamond, but the classes must cooperate.

Use multiple inheritance mainly for:

- Small mixins.
- Independent reusable capabilities.
- Framework-specific patterns.
- Carefully designed cooperative hierarchies.

For most application architecture, composition is easier to maintain.

---

# 13. Abstract Base Classes

An ABC defines a formal class contract.

```
from abc import ABC, abstractmethod
```

```
class Storage(ABC):

    @abstractmethod
    def save(self, data):
        pass
```

Concrete implementation:

```
class FileStorage(Storage):

    def save(self, data):
        return f"Saved {data} to a file."
```

This fails:

```
Storage()
```

because it has an unimplemented abstract method.

This works:

```
storage = FileStorage()

print(storage.save("ticket"))
```

ABCs are useful when:

- You control the hierarchy.
- Subclasses must implement certain methods.
- You want failure at instantiation rather than later.
- Shared parent behavior belongs in the base class.
- The classes are genuinely related.

Python’s `abc` module supplies the machinery for abstract base classes and abstract methods.[[docs.python](https://docs.python.org/3/library/abc.html)]

## ABC versus Protocol

```
ABC:
class CloudProvider(LLMProvider)
```

Explicit inheritance is expected.

```
Protocol:
class CloudProvider:
    def generate(...):
        ...
```

The structure is enough; inheritance is not required.

Use:

```
ABC
```

for formal nominal hierarchies.

Use:

```
Protocol
```

for flexible structural interfaces.

---

# 14. Dataclasses

The `@dataclass` decorator generates common methods from annotated fields, including `__init__()` and `__repr__()`.[[docs.python](https://docs.python.org/3/library/dataclasses.html)]

```
from dataclasses import dataclass
```

```
@dataclass
class Ticket:
    ticket_id: str
    title: str
    priority: str
```

Usage:

```
ticket = Ticket(
    "T-001",
    "Cannot log in",
    "high",
)

print(ticket)
```

Output:

```
Ticket(
    ticket_id='T-001',
    title='Cannot log in',
    priority='high'
)
```

## Default values

```
@dataclass
class User:
    username: str
    active: bool = True
```

## Mutable defaults

Wrong:

```
@dataclass
class Project:
    tasks: list[str] = []
```

Correct:

```
from dataclasses import dataclass, field
```

```
@dataclass
class Project:
    name: str
    tasks: list[str] = field(
        default_factory=list
    )
```

Each instance now gets its own list.

## `__post_init__`

```
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

## Frozen dataclasses

```
@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

```
point = Point(3, 4)
```

Assignment is blocked:

```
point.x = 10
```

Use frozen dataclasses for immutable value objects and configuration.

## Slots

Modern dataclasses can use slots:

```
@dataclass(slots=True)
class Point:
    x: float
    y: float
```

This restricts normal dynamic attributes and may reduce memory usage.

## Dataclass serialization

```
from dataclasses import asdict
import json
```

```
ticket = Ticket(
    "T-001",
    "Cannot log in",
    "high",
)

json_text = json.dumps(
    asdict(ticket),
    indent=2,
)
```

`asdict()` converts the dataclass into a dictionary recursively.

---

# 15. Dataclass comparison

By default, dataclasses generate equality behavior.

```
@dataclass
class Point:
    x: int
    y: int
```

```
print(Point(1, 2) == Point(1, 2))
```

Output:

```
True
```

For immutable hashable value objects:

```
@dataclass(frozen=True)
class Point:
    x: int
    y: int
```

Now:

```
points = {
    Point(1, 2),
    Point(1, 2),
}

print(len(points))
```

Output:

```
1
```

`frozen=True` allows safe hash-like value semantics when all contained fields are themselves suitable.

# 16. Metaclasses

A metaclass is the class of a class.

Normal relationship:

```
object → instance of a class
class   → instance of a metaclass
```

For example:

```
class User:
    pass
```

Then:

```
type(User)
```

returns:

```
<class 'type'>
```

So:

```
User is an instance of type
```

Most classes use:

```
type
```

as their metaclass.

## Classes create objects

When you write:

```
user = User()
```

Python uses the class `User` to create the object.

When Python creates the class `User`, it uses the metaclass `type`.

Conceptually:

```
metaclass creates class
class creates instance
instance contains data
```

---

# 17. A minimal metaclass

```
class LoggedMeta(type):
    def __new__(
        metaclass,
        name,
        bases,
        namespace,
    ):
        print(f"Creating class: {name}")

        return super().__new__(
            metaclass,
            name,
            bases,
            namespace,
        )
```

Use it:

```
class User(metaclass=LoggedMeta):
    pass
```

Output:

```
Creating class: User
```

The metaclass runs when the class is created—not when an instance is created.

```
user = User()
```

This does not print the class-creation message again.

---

# 18. Metaclass validation

A metaclass can validate class definitions.

```
class RequireRunMethod(type):
    def __new__(
        metaclass,
        name,
        bases,
        namespace,
    ):
        if name != "BasePlugin":
            if "run" not in namespace:
                raise TypeError(
                    f"{name} must define run()."
                )

        return super().__new__(
            metaclass,
            name,
            bases,
            namespace,
        )
```

```
class BasePlugin(
    metaclass=RequireRunMethod
):
    pass
```

Valid:

```
class SearchPlugin(BasePlugin):
    def run(self, query):
        return f"Searching for {query}"
```

Invalid:

```
class BrokenPlugin(BasePlugin):
    pass
```

This raises a `TypeError` during class creation.

## Why this can be useful

Metaclasses can enforce:

- Required class methods.
- Naming conventions.
- Registration.
- Field definitions.
- Framework contracts.
- ORM mappings.
- Plugin structures.

But this is advanced and can make code harder to understand.

---

# 19. Metaclass registration

```
class PluginMeta(type):
    registry = {}

    def __new__(
        metaclass,
        name,
        bases,
        namespace,
    ):
        cls = super().__new__(
            metaclass,
            name,
            bases,
            namespace,
        )

        if name != "Plugin":
            metaclass.registry[name] = cls

        return cls
```

```
class Plugin(metaclass=PluginMeta):
    pass
```

```
class SentimentPlugin(Plugin):
    pass
```

```
class TicketPlugin(Plugin):
    pass
```

Inspect:

```
print(PluginMeta.registry)
```

Possible output:

```
{
    'SentimentPlugin': <class ...>,
    'TicketPlugin': <class ...>
}
```

A class decorator often provides the same functionality more simply:

```
PLUGIN_REGISTRY = {}
```

```
def register_plugin(cls):
    PLUGIN_REGISTRY[cls.__name__] = cls
    return cls
```

```
@register_plugin
class SentimentPlugin:
    pass
```

Prefer a class decorator, registry function, or `__init_subclass__()` before reaching for a metaclass.

---

# 20. `__init_subclass__`: often better than a metaclass

Python provides a simpler hook for customizing subclass creation.

```
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

Use:

```
class TicketPlugin(
    Plugin,
    plugin_name="ticket",
):
    def run(self, text):
        return "general"
```

```
print(Plugin.registry)
```

Output:

```
{'ticket': <class '__main__.TicketPlugin'>}
```

`__init_subclass__()` is often enough for:

- Automatic registration.
- Subclass validation.
- Configuration requirements.
- Simple framework hooks.

Use a metaclass only when you need to control or customize class creation at a deeper level.

---

# 21. When to use metaclasses

Use a metaclass when:

- You are building a framework or library.
- You must transform classes as they are created.
- You need class-level registration or validation that simpler hooks cannot provide.
- You understand MRO and metaclass compatibility.
- The behavior applies to many class definitions.
- The metaclass significantly simplifies the framework’s user code.

Examples in the Python ecosystem include:

- ORM model declarations.
- Validation frameworks.
- Abstract base class machinery.
- Plugin frameworks.
- Enum-like systems.
- Framework route or field registration.

Do not use a metaclass merely to:

- Avoid writing a helper function.
- Add one class attribute.
- Register one class.
- Enforce ordinary instance validation.
- Reuse a few methods.
- Make code appear advanced.

Prefer this progression:

```
function
    ↓
class decorator
    ↓
__init_subclass__
    ↓
metaclass
```

Use the simplest mechanism that solves the problem.

---

# 22. Metaclass conflicts

A class can inherit from parents whose metaclasses are incompatible.

```
class MetaA(type):
    pass


class MetaB(type):
    pass


class A(metaclass=MetaA):
    pass


class B(metaclass=MetaB):
    pass
```

This may fail:

```
class C(A, B):
    pass
```

because Python cannot choose a compatible metaclass.

Metaclass conflicts are one reason to avoid unnecessary metaclass design.

ABCs, dataclasses, ORM frameworks, and other advanced libraries may already use metaclasses. Adding another custom metaclass can create compatibility problems.

---

# 23. Complete modern model example

```
from dataclasses import dataclass
from typing import Literal, Protocol
```

Define a precise category:

```
Category = Literal[
    "billing",
    "account_access",
    "technical",
    "general",
]
```

Define the result object:

```
@dataclass(frozen=True)
class ClassificationResult:
    category: Category
    confidence: float
```

Define the provider interface:

```
class Classifier(Protocol):
    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        ...
```

Implement a provider:

```
class KeywordClassifier:
    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        normalized = text.lower()

        if "payment" in normalized:
            return ClassificationResult(
                category="billing",
                confidence=0.96,
            )

        if "password" in normalized:
            return ClassificationResult(
                category="account_access",
                confidence=0.94,
            )

        return ClassificationResult(
            category="general",
            confidence=0.55,
        )
```

Compose it into a service:

```
class TicketService:
    def __init__(
        self,
        classifier: Classifier,
    ):
        self._classifier = classifier

    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        return self._classifier.classify(text)
```

Use:

```
service = TicketService(
    KeywordClassifier()
)

result = service.classify(
    "My payment failed."
)

print(result)
```

Output:

```
ClassificationResult(
    category='billing',
    confidence=0.96
)
```

This design uses:

```
Protocol          → behavior contract
dataclass         → structured immutable result
Literal           → valid categories
composition       → service receives classifier
polymorphism      → any compatible classifier works
```

It avoids unnecessary metaclasses and deep inheritance.

# 24. Common design choices

|Problem|Recommended tool|
|---|---|
|Validate one attribute|Property|
|Reuse validation across classes|Descriptor|
|Create common object methods|Dataclass|
|Define required subclass methods|ABC|
|Describe flexible behavior|Protocol|
|Add class registration|Decorator or `__init_subclass__`|
|Control class creation deeply|Metaclass|
|Combine interchangeable services|Composition|
|Create specialized domain category|Inheritance|
|Make objects work with Python syntax|Dunder methods|

# 25. Practice exercises

## Exercise 1: Value object

Create a `Money` class with:

```
amount
currency
```

Implement:

```
__repr__
__str__
__eq__
__add__
```

Reject addition between different currencies.

## Exercise 2: Descriptor

Create a reusable `NonEmptyString` descriptor that validates string attributes.

Use it for:

```
User.username
Project.name
```

## Exercise 3: MRO

Create:

```
A
B(A)
C(A)
D(B, C)
```

Give every class a `show()` method and inspect:

```
D.mro()
```

## Exercise 4: ABC

Create an abstract `Repository` class requiring:

```
save()
get_by_id()
```

Implement an in-memory repository.

## Exercise 5: Dataclass

Create a frozen dataclass called:

```
ExperimentResult
```

with:

```
model_name
accuracy
samples
```

Validate that accuracy is between `0` and `1`.

## Exercise 6: Metaclass alternative

Create a plugin registry using:

1. A class decorator.
2. `__init_subclass__()`.

Do not use a metaclass initially.

# 26. Final mental model

## Dunder methods

```
Make objects participate in Python syntax.
```

```
len(obj)
obj + other
obj[key]
print(obj)
```

## Properties

```
Make attributes managed.
```

```
obj.price
```

can perform validation and controlled storage.

## Descriptors

```
Reusable attribute-management logic.
```

```
amount = PositiveNumber()
```

## Inheritance

```
Reuse and specialize a genuine parent-child relationship.
```

```
class AdminUser(User):
    ...
```

## `super()`

```
Continue through the inheritance MRO.
```

## ABC

```
Enforce a formal inheritance-based contract.
```

## Dataclass

```
Model structured data with less boilerplate.
```

## Metaclass

```
Customize how classes themselves are created.
```

The practical hierarchy for your projects is:

```
Normal class
    ↓
Dunder methods
    ↓
Properties and descriptors
    ↓
Dataclasses
    ↓
Composition and protocols
    ↓
ABCs
    ↓
__init_subclass__
    ↓
Metaclasses
```

For TrustDesk, Burvex, and future AI systems, prefer:

```
dataclasses for structured domain data
protocols for model/tool/repository interfaces
composition for interchangeable components
ABCs for formal provider hierarchies
descriptors for reusable field rules
metaclasses only for framework-level class creation
```

The most important advanced-object-model principle is:

> Use Python’s protocols to make objects behave naturally, but choose the simplest mechanism that expresses the design clearly.

Dunder methods, descriptors, inheritance, ABCs, dataclasses, and metaclasses are powerful because they integrate with Python’s object model—but that same power means they should be introduced only when the object’s behavior genuinely requires them.[[docs.python](https://docs.python.org/3/reference/datamodel.html?highlight=setattr)][[docs.python](https://docs.python.org/3/howto/descriptor.html)][[docs.python](https://docs.python.org/3/library/dataclasses.html)][[docs.python](https://docs.python.org/3/library/abc.html)]
