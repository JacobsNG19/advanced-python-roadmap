# Modern Type System & Static Typing — Solutions

These solutions correspond to:

```text
Modern Type System & Static Typing - Exercises.md
```

---

## Exercise 1 — Annotated function

```python
def add(first: int, second: int) -> int:
    return first + second
```

---

## Exercise 2 — Optional result

```python
from typing import TypedDict


class User(TypedDict):
    id: str
    username: str


USERS: dict[str, User] = {
    "toussaint": {
        "id": "U-001",
        "username": "toussaint",
    }
}


def find_user(username: str) -> User | None:
    return USERS.get(username)
```

The caller must handle the possibility of `None`:

```python
user = find_user("unknown")

if user is not None:
    print(user["username"])
```

---

## Exercise 3 — Union narrowing

```python
def format_value(value: int | str) -> str:
    if isinstance(value, int):
        return f"Integer: {value}"

    return f"Text: {value.upper()}"
```

The `isinstance()` check narrows the union.

---

## Exercise 4 — Unknown input

```python
def display(value: object) -> str:
    return str(value)
```

`object` accepts any value but does not permit arbitrary operations. `Any` would weaken static checking.

---

## Exercise 5 — Generic first item

```python
from typing import TypeVar


T = TypeVar("T")


def first_item(values: list[T]) -> T:
    if not values:
        raise ValueError("List cannot be empty.")

    return values[0]
```

---

## Exercise 6 — Generic box

```python
from typing import Generic, TypeVar


T = TypeVar("T")


class Box(Generic[T]):
    def __init__(self, value: T):
        self._value = value

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value


box = Box[int](10)
box.set(20)
assert box.get() == 20
```

A checker should reject assigning a string to `Box[int]`.

---

## Exercise 7 — Generic repository

```python
from typing import Generic, TypeVar


Entity = TypeVar("Entity")
ID = TypeVar("ID")


class Repository(Generic[Entity, ID]):
    def __init__(self):
        self._items: dict[ID, Entity] = {}

    def save(self, item_id: ID, item: Entity) -> None:
        self._items[item_id] = item

    def get(self, item_id: ID) -> Entity | None:
        return self._items.get(item_id)
```

Example:

```python
from dataclasses import dataclass


@dataclass
class Ticket:
    title: str


repository = Repository[Ticket, str]()
repository.save("T-001", Ticket("Cannot log in"))
```

---

## Exercise 8 — Typed ticket dictionary

```python
from typing import TypedDict


class Ticket(TypedDict):
    id: str
    title: str
    priority: str


ticket: Ticket = {
    "id": "T-001",
    "title": "Cannot log in",
    "priority": "high",
}
```

---

## Exercise 9 — Allowed literal values

```python
from typing import Literal, TypedDict


Priority = Literal[
    "low",
    "normal",
    "high",
]


class Ticket(TypedDict):
    id: str
    title: str
    priority: Priority


def create_ticket(
    ticket_id: str,
    title: str,
    priority: Priority,
) -> Ticket:
    return {
        "id": ticket_id,
        "title": title,
        "priority": priority,
    }
```

`Literal` improves static checking; runtime validation is still needed for external data.

---

## Exercise 10 — Optional dictionary key

```python
from typing import NotRequired, TypedDict


class User(TypedDict):
    username: str
    email: str
    phone: NotRequired[str]
```

The `phone` key may be absent.

---

## Exercise 11 — Tagged response union

```python
from typing import Literal, TypedDict


class SuccessResponse(TypedDict):
    status: Literal["success"]
    data: dict[str, str]


class ErrorResponse(TypedDict):
    status: Literal["error"]
    message: str


Response = SuccessResponse | ErrorResponse


def handle_response(response: Response) -> str:
    if response["status"] == "success":
        return f"Data: {response['data']}"

    return f"Error: {response['message']}"
```

The `status` value acts as a discriminator.

---

## Exercise 12 — Protocol for notifications

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


def alert(
    notifier: Notifier,
    message: str,
) -> str:
    return notifier.send(message)
```

The implementations do not inherit from `Notifier`; they satisfy it structurally.

---

## Exercise 13 — Protocol with attributes

```python
from typing import Protocol


class ModelProvider(Protocol):
    name: str

    def generate(self, prompt: str) -> str:
        ...


class LocalProvider:
    name = "local-model-v1"

    def generate(self, prompt: str) -> str:
        return f"{self.name}: {prompt}"
```

---

## Exercise 14 — Generic protocol

```python
from typing import Protocol, TypeVar


Input = TypeVar("Input")
Output = TypeVar("Output")


class Transformer(Protocol[Input, Output]):
    def transform(self, value: Input) -> Output:
        ...


class TextLength:
    def transform(self, value: str) -> int:
        return len(value)


def apply_transformer(
    transformer: Transformer[str, int],
    value: str,
) -> int:
    return transformer.transform(value)
```

---

## Exercise 15 — Annotated metadata

```python
from typing import Annotated, get_args, get_origin


Username = Annotated[
    str,
    "minimum length: 3",
]


assert get_origin(Username) is Annotated
assert get_args(Username) == (
    str,
    "minimum length: 3",
)
```

The metadata does not validate values automatically.

---

## Exercise 16 — Runtime input validation

```python
from typing import Literal, TypedDict


Priority = Literal[
    "low",
    "normal",
    "high",
]


class Ticket(TypedDict):
    id: str
    title: str
    priority: Priority


def parse_ticket(data: object) -> Ticket:
    if not isinstance(data, dict):
        raise ValueError("Ticket must be a dictionary.")

    ticket_id = data.get("id")
    title = data.get("title")
    priority = data.get("priority")

    if not isinstance(ticket_id, str):
        raise ValueError("id must be a string.")

    if not isinstance(title, str):
        raise ValueError("title must be a string.")

    if priority not in {"low", "normal", "high"}:
        raise ValueError("Invalid priority.")

    return {
        "id": ticket_id,
        "title": title,
        "priority": priority,
    }
```

This validates external data before returning the precise internal type.

---

## Exercise 17 — Custom type narrowing

```python
from typing import TypeGuard


def is_string_list(
    values: list[object],
) -> TypeGuard[list[str]]:
    return all(
        isinstance(value, str)
        for value in values
    )


values: list[object] = ["Python", "AI"]

if is_string_list(values):
    uppercase = [value.upper() for value in values]
```

Inside the conditional branch, the checker understands `values` as `list[str]`.

---

## Exercise 18 — Distinct IDs

```python
from typing import NewType


UserID = NewType("UserID", str)
TicketID = NewType("TicketID", str)


def get_ticket(ticket_id: TicketID) -> str:
    return f"Ticket: {ticket_id}"


ticket_id = TicketID("T-001")
assert get_ticket(ticket_id) == "Ticket: T-001"
```

A static checker can distinguish `UserID` from `TicketID`, even though both are strings at runtime.

---

## Exercise 19 — Immutable constant and class field

```python
from typing import ClassVar, Final


MAX_RETRIES: Final[int] = 3


class User:
    platform: ClassVar[str] = "TrustDesk"

    def __init__(self, username: str):
        self.username = username
```

`Final` communicates that reassignment is not intended. `ClassVar` indicates that `platform` belongs to the class.

---

## Exercise 20 — Fluent API

```python
from typing import Self


class Query:
    def __init__(self):
        self.parts: list[str] = []

    def where(self, expression: str) -> Self:
        self.parts.append(expression)
        return self

    def limit(self, amount: int) -> Self:
        self.parts.append(f"LIMIT {amount}")
        return self


query = (
    Query()
    .where("priority = 'high'")
    .limit(10)
)
```

`Self` preserves the concrete class type in fluent APIs.

---

## Exercise 21 — Overloaded function

```python
from typing import overload


@overload
def parse_value(value: int) -> int:
    ...


@overload
def parse_value(value: str) -> str:
    ...


def parse_value(value: int | str) -> int | str:
    if isinstance(value, int):
        return value

    return value.strip()
```

The overloads describe the public input/output relationships. The final function is the runtime implementation.

---

## Exercise 22 — Typed decorator

```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


def log_call(
    function: Callable[P, R],
) -> Callable[P, R]:
    @wraps(function)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        print(f"Calling {function.__name__}")
        return function(*args, **kwargs)

    return wrapper
```

`ParamSpec` preserves the wrapped function's parameter structure.

---

## Exercise 23 — Typed model result

```python
from dataclasses import dataclass
from typing import Literal


Category = Literal[
    "billing",
    "account_access",
    "technical",
    "general",
]


@dataclass(frozen=True)
class ClassificationResult:
    category: Category
    confidence: float

    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )
```

The `Literal` restricts categories for static checking; `__post_init__()` validates the confidence at runtime.

---

## Exercise 24 — Static checker configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"

[tool.ruff]
line-length = 79
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.pyright]
include = ["src", "tests"]
typeCheckingMode = "standard"
pythonVersion = "3.12"
```

Run:

```bash
ruff check .
ruff format --check .
pyright
pytest
```

---

## Exercise 25 — Final typed AI service

```python
from dataclasses import dataclass
from typing import Literal, Protocol


Category = Literal[
    "billing",
    "account_access",
    "technical",
    "general",
]


@dataclass(frozen=True)
class ClassificationResult:
    category: Category
    confidence: float

    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )


class Classifier(Protocol):
    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        ...


class KeywordClassifier:
    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        if not text.strip():
            raise ValueError("Text cannot be empty.")

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


class TicketService:
    def __init__(self, classifier: Classifier):
        self._classifier = classifier

    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        return self._classifier.classify(text)


class FakeClassifier:
    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        return ClassificationResult(
            category="general",
            confidence=1.0,
        )


service = TicketService(KeywordClassifier())
result = service.classify("My payment failed")

assert result.category == "billing"

fake_service = TicketService(FakeClassifier())
fake_result = fake_service.classify("Test")

assert fake_result.category == "general"
```

The service depends on the `Classifier` behavior, not on a particular concrete classifier.

---

# Review checklist

You should now understand:

- Generic functions and classes.
- `TypeVar` relationships.
- Structural Protocols.
- `TypedDict` data shapes.
- Literal value restrictions.
- Optional keys versus nullable values.
- Annotated metadata.
- Runtime validation boundaries.
- Type narrowing and `TypeGuard`.
- `NewType`, `Final`, `ClassVar`, and `Self`.
- Overloads and typed decorators.
- Static checker configuration.
