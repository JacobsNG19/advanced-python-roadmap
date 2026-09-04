Modern typing has four layers:

```
Type hints        → describe intended types
Generics          → write reusable type-safe code
Protocols         → describe behavior structurally
Static checkers   → detect inconsistencies before execution
Runtime checks    → validate real external data
```

For your AI-engineering projects, use precise types internally, validate untrusted boundaries at runtime, and use `mypy`, `pyright`, or `ty` continuously rather than treating typing as documentation added at the end.

# 1. Static typing versus runtime typing

Python does not normally enforce annotations automatically:

```
def greet(name: str) -> str:
    return f"Hello, {name}"
```

This may still execute:

```
greet(123)
```

A static checker can report the mismatch before the program runs.

```
Static checker → analyzes source code
Runtime validation → checks actual values while running
```

Use static typing for:

- Function contracts.
- Data structures.
- Service interfaces.
- Refactoring safety.
- IDE support.
- Detecting wrong arguments and return values.

Use runtime validation for:

- HTTP requests.
- JSON.
- CLI input.
- Environment variables.
- Database rows.
- LLM-generated output.
- User uploads.
- Webhooks.

The `typing` system is mainly for type checkers and tools; Python itself generally does not enforce annotations.[[cs.georgefox](https://cs.georgefox.edu/hs_contest/docs/python-3.10.12-docs/library/typing.html)]

# 2. `TypeVar`: reusable relationships

A `TypeVar` represents a type that remains consistent across a function or class.

```
from typing import TypeVar

T = TypeVar("T")
```

## Generic function

```
def first_item(items: list[T]) -> T:
    return items[0]
```

The type checker understands:

```
number = first_item([1, 2, 3])
```

as:

```
number: int
```

And:

```
name = first_item(["A", "B"])
```

as:

```
name: str
```

The function preserves the relationship:

```
list[T] → T
```

Without a type variable:

```
def first_item(items: list[Any]) -> Any:
    ...
```

you lose that relationship.

## Generic identity function

```
def identity(value: T) -> T:
    return value
```

```
number = identity(10)
text = identity("hello")
```

The result keeps the input type.

---

# 3. Constrained and bound type variables

## Constrained `TypeVar`

```
from typing import TypeVar

Text = TypeVar(
    "Text",
    str,
    bytes,
)
```

```
def uppercase(value: Text) -> Text:
    return value.upper()
```

This allows:

```
uppercase("hello")
uppercase(b"hello")
```

A constrained type variable accepts one of a fixed set of types.

## Bound `TypeVar`

```
Number = TypeVar(
    "Number",
    bound=int,
)
```

This means the type must be `int` or a subtype of `int`.

More useful example:

```
from collections.abc import Sized
from typing import TypeVar

SizedObject = TypeVar(
    "SizedObject",
    bound=Sized,
)
```

```
def get_size(value: SizedObject) -> int:
    return len(value)
```

The object must support the `Sized` protocol.

Use:

```
Constrained TypeVar → one of specific types
Bound TypeVar       → any subtype of a base type/protocol
```

The typing specification defines `TypeVar` as a parameter for generic functions, classes, and aliases, with support for constraints and bounds.[[typing.python](https://typing.python.org/en/latest/spec/generics.html)]

---

# 4. Generic classes

A generic class works with a type parameter.

```
from typing import Generic, TypeVar

T = TypeVar("T")
```

```
class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value
```

Use:

```
integer_box = Box[int](10)
string_box = Box[str]("hello")
```

Now:

```
integer_value = integer_box.get()
string_value = string_box.get()
```

The checker understands:

```
integer_value → int
string_value  → str
```

Modern Python can use type-parameter syntax:

```
class Box[T]:
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value
```

This newer syntax is clearer when targeting a sufficiently recent Python version. Mypy documents both generic classes using `TypeVar`/`Generic` and newer type-parameter syntax.[[mypy.readthedocs](https://mypy.readthedocs.io/en/stable/generics.html)]

---

# 5. Generic repository

This pattern is useful for your startup projects.

```
from typing import Generic, TypeVar

Entity = TypeVar("Entity")
ID = TypeVar("ID")
```

```
class Repository(Generic[Entity, ID]):
    def __init__(self):
        self._items: dict[ID, Entity] = {}

    def save(self, item_id: ID, item: Entity) -> None:
        self._items[item_id] = item

    def get(self, item_id: ID) -> Entity | None:
        return self._items.get(item_id)
```

Use with a dataclass:

```
from dataclasses import dataclass


@dataclass
class Ticket:
    title: str
    priority: str
```

```
ticket_repository = Repository[Ticket, str]()

ticket_repository.save(
    "T-001",
    Ticket(
        title="Cannot log in",
        priority="high",
    ),
)

ticket = ticket_repository.get("T-001")
```

The checker understands:

```
ticket → Ticket | None
```

It can also detect:

```
ticket_repository.save(
    100,
    "not a Ticket",
)
```

because the repository expects:

```
ID = str
Entity = Ticket
```

---

# 6. `Self`

`Self` represents the current class type.

```
from typing import Self
```

```
class Query:
    def __init__(self, text: str):
        self.text = text

    def normalize(self) -> Self:
        self.text = self.text.strip().lower()
        return self
```

Use:

```
query = (
    Query("  Python  ")
    .normalize()
)
```

For subclasses, `Self` preserves the subclass type better than returning the parent class explicitly.

```
class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self
```

This supports fluent APIs:

```
builder = (
    Builder()
    .set_name("TrustDesk")
)
```

The typing specification describes `Self` as automatically representing the current class type in methods and class methods.[[typing.python](https://typing.python.org/en/latest/reference/generics.html)]

---

# 7. `Protocol`: structural subtyping

A protocol describes behavior without requiring inheritance.

```
from typing import Protocol


class LLMProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```

Implementation:

```
class LocalProvider:
    def generate(self, prompt: str) -> str:
        return f"Local response: {prompt}"
```

No inheritance is needed:

```
class CloudProvider:
    def generate(self, prompt: str) -> str:
        return f"Cloud response: {prompt}"
```

Use the protocol:

```
def answer(
    provider: LLMProvider,
    question: str,
) -> str:
    return provider.generate(question)
```

Both work:

```
answer(LocalProvider(), "What is Python?")
answer(CloudProvider(), "What is Python?")
```

## Structural versus nominal typing

### Nominal typing

The relationship is explicitly declared:

```
class CloudProvider(LLMProvider):
    ...
```

The class is compatible because it inherits from `LLMProvider`.

### Structural typing

The class is compatible because it has the required shape:

```
class CloudProvider:
    def generate(self, prompt: str) -> str:
        ...
```

No inheritance is necessary.

```
ABC        → nominal relationship
Protocol   → structural relationship
```

Protocols are especially useful for:

- Model providers.
- Repositories.
- Cache systems.
- Agent tools.
- Notification systems.
- Test doubles.
- Third-party integrations.

---

# 8. Protocol with attributes

Protocols can require attributes and methods.

```
class ModelProvider(Protocol):
    name: str

    def generate(self, prompt: str) -> str:
        ...
```

Compatible implementation:

```
class LocalModel:
    name = "local-model-v1"

    def generate(self, prompt: str) -> str:
        return f"{self.name}: {prompt}"
```

Use:

```
def describe(provider: ModelProvider) -> str:
    return f"Using {provider.name}"
```

The protocol specifies the minimum behavior needed by the consumer.

That is important:

```
A protocol should describe what the user of the object needs,
not every capability the object happens to have.
```

---

# 9. Generic protocols

A protocol can also be generic.

```
from typing import Protocol, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")
```

```
class Transformer(
    Protocol[Input, Output]
):
    def transform(self, value: Input) -> Output:
        ...
```

Implementation:

```
class TextLength:
    def transform(self, value: str) -> int:
        return len(value)
```

Use:

```
def apply_transformer(
    transformer: Transformer[str, int],
    value: str,
) -> int:
    return transformer.transform(value)
```

```
length = apply_transformer(
    TextLength(),
    "TrustDesk",
)
```

The protocol describes:

```
str → int
```

This is useful for:

- Data preprocessing.
- Serialization.
- Model pipelines.
- Input/output adapters.
- Generic repository interfaces.

# 10. `TypedDict`

`TypedDict` describes dictionary-shaped data.

```
from typing import TypedDict


class Ticket(TypedDict):
    id: str
    title: str
    priority: str
```

```
ticket: Ticket = {
    "id": "T-001",
    "title": "Cannot log in",
    "priority": "high",
}
```

A static checker can detect missing keys and wrong value types.

`TypedDict` remains a normal dictionary at runtime. Its required-key expectations are generally enforced by type checkers, not automatically at runtime.[[cs.georgefox](https://cs.georgefox.edu/hs_contest/docs/python-3.10.12-docs/library/typing.html)]

## TypedDict with `Literal`

```
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
```

Now this is statically invalid:

```
ticket: Ticket = {
    "id": "T-001",
    "title": "Cannot log in",
    "priority": "urgent",
}
```

## Optional keys

```
from typing import NotRequired


class Ticket(TypedDict):
    id: str
    title: str
    priority: Priority
    explanation: NotRequired[str]
```

This means:

```
The explanation key may be absent.
```

That differs from:

```
explanation: str | None
```

which means:

```
The key exists, but its value may be None.
```

---

# 11. Tagged unions

Use `Literal` and `TypedDict` together for different response shapes.

```
from typing import Literal, TypedDict


class SuccessResponse(TypedDict):
    status: Literal["success"]
    data: dict[str, str]


class ErrorResponse(TypedDict):
    status: Literal["error"]
    message: str


Response = SuccessResponse | ErrorResponse
```

```
def handle_response(response: Response) -> str:
    if response["status"] == "success":
        return f"Data: {response['data']}"

    return f"Error: {response['message']}"
```

The `status` field is a discriminator:

```
"success" → SuccessResponse
"error"   → ErrorResponse
```

This is excellent for:

- API responses.
- Agent tool results.
- Model outputs.
- Validation results.
- Event messages.

# 12. `Annotated`

`Annotated` attaches metadata to an existing type.

```
from typing import Annotated
```

```
UserID = Annotated[
    str,
    "Must be a non-empty user identifier",
]
```

The underlying type is still:

```
str
```

The metadata is extra information for a framework, validator, documentation tool, or application.

Python’s typing documentation describes `Annotated[T, metadata]` as a way to attach context-specific metadata while allowing ordinary type checkers to treat the value primarily as `T`.[[cs.georgefox](https://cs.georgefox.edu/hs_contest/docs/python-3.10.12-docs/library/typing.html)]

## Example with validation metadata

```
from dataclasses import dataclass
from typing import Annotated


Positive = "must be greater than zero"
```

```
@dataclass
class Product:
    price: Annotated[
        float,
        Positive,
    ]
```

A normal type checker still sees:

```
price: float
```

It does not automatically enforce the string metadata.

A validation framework could inspect it:

```
from typing import get_args, get_origin


annotation = Product.__annotations__["price"]

print(get_origin(annotation))
print(get_args(annotation))
```

Possible output:

```
<class 'typing.Annotated'>
(<class 'float'>, 'must be greater than zero')
```

## Practical framework example

Some frameworks use metadata:

```
from typing import Annotated


def min_length(length: int):
    return {
        "min_length": length,
    }
```

```
Username = Annotated[
    str,
    min_length(3),
]
```

A framework can inspect the metadata and perform runtime validation.

Without framework logic, `Annotated` is only metadata.

---

# 13. `Annotated` versus comments

This:

```
username: str  # at least 3 characters
```

is a human comment.

This:

```
username: Annotated[
    str,
    "minimum length: 3",
]
```

is machine-readable metadata.

But metadata has meaning only if a tool or your own code interprets it.

Use `Annotated` when:

- A framework supports it.
- You are building a validation or dependency-injection system.
- You want machine-readable field metadata.
- A library’s API explicitly expects it.

Do not add arbitrary metadata everywhere without a consumer.

---

# 14. `Any`, `object`, and `Unknown`

## `Any`

`Any` disables many static checks.

```
from typing import Any


def process(value: Any):
    return value.any_method()
```

The checker may allow this, but runtime may fail.

## `object`

`object` means any Python object, but unlike `Any`, you cannot call arbitrary methods on it.

```
def display(value: object) -> str:
    return str(value)
```

This is safe because every object supports string conversion.

This is not accepted:

```
def bad(value: object):
    return value.upper()
```

The checker rejects it because `object` is not known to have `.upper()`.

## Practical distinction

```
Any    → trust this value; type checking is weakened
object → any value; prove capabilities before using them
```

Prefer `object` when you genuinely accept any value but still want type safety.

# 15. Type narrowing

A union must be narrowed before type-specific operations.

```
def format_value(value: int | str) -> str:
    if isinstance(value, int):
        return f"Number: {value}"

    return value.upper()
```

The checker understands:

```
if branch → int
else branch → str
```

Other narrowing patterns:

```
if value is None:
    ...
```

```
if isinstance(value, dict):
    ...
```

```
if "status" in response:
    ...
```

```
match response:
    case {"status": "success"}:
        ...
```

For tagged unions, checking a literal discriminator is particularly useful.

# 16. `TypeGuard`

A custom validator can tell the type checker that a condition narrows a type.

```
from typing import TypeGuard


def is_string_list(
    value: list[object],
) -> TypeGuard[list[str]]:
    return all(
        isinstance(item, str)
        for item in value
    )
```

Use:

```
values: list[object] = [
    "AI",
    "Python",
]

if is_string_list(values):
    for value in values:
        print(value.upper())
```

Inside the `if` block, the checker understands:

```
values: list[str]
```

`TypeGuard` is useful when ordinary `isinstance()` checks are not enough.

# 17. `TypeIs`

Newer typing systems also support `TypeIs` for type predicates that establish a narrower relationship more precisely.

```
from typing import TypeIs
```

```
def is_positive(
    value: int | float,
) -> TypeIs[int | float]:
    return value > 0
```

In normal application code, `TypeGuard` is enough to learn first. Use `TypeIs` when your checker and Python version support it and you need its more precise narrowing semantics.

# 18. `NewType`

`NewType` creates a static distinction between logically different values that share a runtime type.

```
from typing import NewType


UserID = NewType("UserID", str)
TicketID = NewType("TicketID", str)
```

```
def get_ticket(ticket_id: TicketID):
    ...
```

This can catch accidentally passing:

```
user_id: UserID
```

where:

```
TicketID
```

is expected.

At runtime, `UserID("U-001")` behaves essentially like a string. `NewType` mainly helps static analysis.

# 19. Overloads

Use `@overload` when the return type depends on the input type.

```
from typing import overload


@overload
def parse_id(value: int) -> int:
    ...


@overload
def parse_id(value: str) -> str:
    ...


def parse_id(value: int | str) -> int | str:
    if isinstance(value, int):
        return value

    return value.strip()
```

The implementation signature handles all cases, while overloads describe the public relationships to a type checker.

This is useful when:

```
input type A → output type X
input type B → output type Y
```

Do not use overloads when a normal union return is sufficient.

# 20. `Final` and `ClassVar`

## `Final`

```
from typing import Final


MAX_RETRIES: Final = 3
```

A type checker warns if you reassign it:

```
MAX_RETRIES = 5
```

For class attributes:

```
class Config:
    DEFAULT_TIMEOUT: Final[int] = 30
```

`Final` communicates that the value should not be reassigned.

It does not create runtime immutability.

## `ClassVar`

```
from typing import ClassVar


class User:
    total_users: ClassVar[int] = 0
```

`ClassVar` tells the checker that an attribute belongs to the class, not each instance.

This is useful with dataclasses:

```
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class User:
    username: str
    platform: ClassVar[str] = "TrustDesk"
```

# 21. Variance: practical introduction

Variance describes how generic subtypes relate.

You mainly need these ideas:

```
Invariant  → exact generic type relationship
Covariant  → safely produces values
Contravariant → safely consumes values
```

## Invariance

Mutable lists are generally invariant:

```
list[Dog]
```

is not safely interchangeable with:

```
list[Animal]
```

because someone could insert a `Cat` into a list expected to contain only dogs.

## Covariance

A read-only sequence can safely produce more specific objects:

```
from collections.abc import Sequence


def display_animals(
    animals: Sequence[Animal],
) -> None:
    ...
```

A sequence of dogs can often be used because the function only reads from it.

## Contravariance

A consumer that can handle general objects may be used where a consumer of a narrower object is needed.

You do not need to design custom variance immediately. Understand the safety reason:

```
Read-only producers are more flexible.
Mutable containers are more restrictive.
```

# 22. Type aliases

Use aliases to name complex types.

```
from typing import TypeAlias, Literal


Priority: TypeAlias = Literal[
    "low",
    "normal",
    "high",
]
```

```
JSONValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | list["JSONValue"]
    | dict[str, "JSONValue"]
)
```

Recursive aliases can describe JSON-like values:

```
def save_json(value: JSONValue) -> None:
    ...
```

Named aliases are easier to read than repeating large unions everywhere.

# 23. Runtime checking patterns

Static typing does not validate external data.

Use runtime checks at boundaries.

## Simple `isinstance`

```
def parse_limit(value: object) -> int:
    if not isinstance(value, int):
        raise TypeError(
            "limit must be an integer."
        )

    if value <= 0:
        raise ValueError(
            "limit must be positive."
        )

    return value
```

Use `object` rather than `Any` when the value is unknown but you want to prove its type.

## Dictionary boundary

```
from typing import Any, cast


def parse_ticket(data: Any) -> Ticket:
    if not isinstance(data, dict):
        raise ValueError(
            "Ticket must be an object."
        )

    ticket_id = data.get("id")
    title = data.get("title")
    priority = data.get("priority")

    if not isinstance(ticket_id, str):
        raise ValueError("id must be a string.")

    if not isinstance(title, str):
        raise ValueError(
            "title must be a string."
        )

    if priority not in {
        "low",
        "normal",
        "high",
    }:
        raise ValueError(
            "Invalid priority."
        )

    return {
        "id": ticket_id,
        "title": title,
        "priority": priority,
    }
```

Do not use `cast()` as validation.

# 24. `cast()` is not validation

```
from typing import cast


value = cast(str, unknown_value)
```

`cast()` tells the type checker:

```
Treat this as a string.
```

It does not convert or validate the value.

```
value = cast(str, 123)
```

At runtime, `value` remains:

```
123
```

Use `cast()` only when you already know the value is correct and the checker cannot infer it.

Bad:

```
data = cast(Ticket, external_json)
```

Better:

```
data = parse_ticket(external_json)
```

# 25. `runtime_checkable` protocols

```
from typing import Protocol, runtime_checkable


@runtime_checkable
class Closable(Protocol):
    def close(self) -> None:
        ...
```

```
class Resource:
    def close(self) -> None:
        print("Closed.")
```

```
resource = Resource()

print(isinstance(resource, Closable))
```

Output:

```
True
```

Runtime-checkable protocols mainly check whether required attributes exist. They do not fully validate method signatures or behavior.

Use them for simple capability checks:

```
if isinstance(resource, Closable):
    resource.close()
```

Do not treat them as a replacement for full runtime validation.

# 26. Mypy effectively

Install:

```
python -m pip install mypy
```

Run:

```
mypy src/
```

A basic configuration in `pyproject.toml`:

```
[tool.mypy]
python_version = "3.12"
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
```

For a new, well-typed project:

```
[tool.mypy]
python_version = "3.12"
strict = true
```

Strict mode can be valuable, but do not force it immediately on a large untyped codebase.

## Gradual mypy workflow

```
1. Annotate public functions.
2. Run mypy.
3. Fix real errors.
4. Reduce Any.
5. Enable more warnings.
6. Move toward strict mode.
```

Important mypy checks include:

- Incompatible argument types.
- Incompatible return values.
- Missing returns.
- Missing attributes.
- Incorrect dictionary keys.
- Protocol mismatches.
- Unchecked imports.
- Unused `type: ignore` comments.

Mypy’s documentation notes that unannotated functions receive less useful analysis, which is why annotating public interfaces is a high-value first step.[[mypy.readthedocs](https://mypy.readthedocs.io/en/stable/getting_started.html)]

# 27. Pyright effectively

Install:

```
python -m pip install pyright
```

Run:

```
pyright
```

Configuration:

```
{
  "include": ["src"],
  "exclude": ["**/__pycache__"],
  "typeCheckingMode": "standard",
  "pythonVersion": "3.12"
}
```

Modes commonly include:

```
off
basic
standard
strict
```

For VS Code, Pyright-based Pylance provides immediate editor diagnostics.

Use Pyright when:

- You want excellent editor feedback.
- You use VS Code heavily.
- You want fast analysis.
- You are working on a large source tree.
- You prefer configurable per-rule diagnostics.

# 28. `ty` effectively

`ty` is Astral’s fast Python type checker and language server. The official documentation shows:

```
uvx ty check
```

as a quick way to run it, and:

```
ty check
```

for project checking.[[docs.astral](https://docs.astral.sh/ty/)][[docs.astral](https://docs.astral.sh/ty/type-checking/)]

Install as a project development tool:

```
uv add --dev ty
```

Run:

```
uv run ty check
```

Or install globally:

```
uv tool install ty
```

Then:

```
ty check
```

Target a path:

```
ty check src/
```

Watch mode:

```
ty check --watch
```

Configuration in `pyproject.toml`:

```
[tool.ty.environment]
python-version = "3.12"

[tool.ty.rules]
unresolved-import = "error"
unused-ignore-comment = "warn"
```

`ty` configures individual rules with severities such as:

```
ignore
warn
error
```

rather than relying only on one global strictness preset.[[docs.astral](https://docs.astral.sh/ty/reference/configuration/)]

# 29. Which checker should you use?

|Tool|Strong choice when|
|---|---|
|Mypy|You want a mature, explicit command-line checker|
|Pyright|You use VS Code and want fast editor feedback|
|ty|You want a fast modern checker integrated with Astral’s tooling|
|More than one|You are maintaining a library or comparing compatibility|

For learning, choose one primary checker:

```
VS Code-heavy workflow → Pyright/Pylance
CLI/CI-heavy workflow  → mypy
Astral/uv/Ruff workflow → ty
```

Do not begin by running all three and trying to satisfy every difference. Pick one, establish a clean baseline, then compare later.

# 30. Strictness and gradual adoption

A practical progression:

## Stage 1: annotate public APIs

```
def classify(
    text: str,
) -> ClassificationResult:
    ...
```

## Stage 2: type structured data

```
TypedDict
dataclass
Protocol
Literal
```

## Stage 3: eliminate accidental `Any`

Replace:

```
data: Any
```

with:

```
data: object
```

then validate and narrow it.

## Stage 4: enable stricter rules

Mypy:

```
mypy --strict src/
```

Pyright:

```
{
  "typeCheckingMode": "strict"
}
```

ty:

```
[tool.ty.rules]
invalid-assignment = "error"
possibly-unresolved-reference = "error"
```

## Stage 5: add CI

```
python -m mypy src/
python -m pytest
```

or:

```
pyright
pytest
```

or:

```
ty check
pytest
```

# 31. Static typing in CI

A GitHub Actions-style command:

```
- name: Type check
  run: python -m mypy src/

- name: Test
  run: python -m pytest
```

The important principle:

```
A type checker should run against the same Python version and dependencies
used by the project.
```

Otherwise, the checker may report false import or compatibility errors.

# 32. Runtime validation architecture

For an AI API:

```
untrusted request
        ↓
runtime validation
        ↓
typed internal object
        ↓
business logic
        ↓
typed response
        ↓
JSON serialization
```

Example:

```
from dataclasses import dataclass


@dataclass
class CreateTicketRequest:
    title: str
    priority: Priority
```

Runtime parser:

```
def parse_request(
    data: object,
) -> CreateTicketRequest:
    if not isinstance(data, dict):
        raise ValueError(
            "Request must be an object."
        )

    title = data.get("title")
    priority = data.get("priority")

    if not isinstance(title, str):
        raise ValueError(
            "title must be a string."
        )

    if priority not in {
        "low",
        "normal",
        "high",
    }:
        raise ValueError(
            "Invalid priority."
        )

    return CreateTicketRequest(
        title=title,
        priority=priority,
    )
```

After parsing, the rest of the code can safely use:

```
request.title
request.priority
```

For large schemas, use a runtime validation library, but preserve precise Python annotations in the application layer.

# 33. Runtime type checking: when useful

Use runtime checks when data crosses a trust or system boundary:

- HTTP request body.
- CLI arguments.
- Environment variables.
- Database response.
- File contents.
- Webhook payload.
- LLM output.
- Plugin input.
- User-supplied configuration.

Do not add runtime checks to every internal function if static typing and controlled construction already guarantee the type.

Bad overchecking:

```
def add(first: int, second: int) -> int:
    if not isinstance(first, int):
        raise TypeError(...)

    if not isinstance(second, int):
        raise TypeError(...)

    return first + second
```

This may be appropriate for a public library boundary, but often unnecessary in a private, typed internal module.

Use:

```
Static checking inside trusted code.
Runtime validation at untrusted boundaries.
```

# 34. Common mistakes

## Treating annotations as validation

```
def create_user(age: int):
    ...
```

does not guarantee runtime input is an integer.

## Using `Any` as a permanent solution

```
def process(data: Any) -> Any:
    ...
```

This prevents the checker from helping.

## Using `cast()` instead of validation

```
ticket = cast(Ticket, external_data)
```

does not inspect the data.

## Oversized protocols

Do not require every model provider to implement:

```
generate
embed
rerank
search
train
save
delete
```

if the consumer only needs:

```
generate
```

## Confusing `TypedDict` and dataclasses

```
TypedDict → dictionary data shape
dataclass → runtime object with behavior
```

## Overusing generics

Not every function needs `TypeVar`.

Use generics when a type relationship must be preserved:

```
list[T] → T
```

## Running multiple checkers without a plan

Mypy, Pyright, and ty may make different decisions or report different diagnostics. Establish one primary checker first.

# 35. Complete typed architecture

```
from dataclasses import dataclass
from typing import Literal, Protocol
```

Domain type:

```
Category = Literal[
    "billing",
    "account_access",
    "technical",
    "general",
]
```

Result object:

```
@dataclass(frozen=True)
class ClassificationResult:
    category: Category
    confidence: float
```

Protocol:

```
class Classifier(Protocol):
    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        ...
```

Implementation:

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

Service:

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
        if not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        return self._classifier.classify(text)
```

Test double:

```
class FakeClassifier:
    def classify(
        self,
        text: str,
    ) -> ClassificationResult:
        return ClassificationResult(
            category="general",
            confidence=1.0,
        )
```

The static checker verifies the fake classifier satisfies the protocol even though it does not inherit from it.

# 36. Final cheat sheet

## Generic function

```
T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]
```

## Generic class

```
class Box[T]:
    def __init__(self, value: T):
        self.value = value
```

## Protocol

```
class Tool(Protocol):
    def run(self, input_text: str) -> str:
        ...
```

## Typed dictionary

```
class Ticket(TypedDict):
    id: str
    title: str
```

## Literal

```
Priority = Literal[
    "low",
    "normal",
    "high",
]
```

## Annotated

```
Username = Annotated[
    str,
    "minimum length: 3",
]
```

Metadata requires a framework or your own code to interpret it.

## Type narrowing

```
if isinstance(value, str):
    ...
```

## Runtime validation

```
def parse(data: object) -> Ticket:
    if not isinstance(data, dict):
        raise ValueError(...)
    ...
```

## Mypy

```
mypy src/
```

## Pyright

```
pyright
```

## ty

```
ty check
```

The central architecture to remember is:

```
TypeVar       → preserve relationships between types
Generics      → reusable typed containers and algorithms
Protocol      → structural behavior contracts
TypedDict     → typed dictionary-shaped data
Literal       → finite allowed values
Annotated     → type plus metadata
TypeGuard     → custom narrowing
Any           → dynamic escape hatch
Runtime checks → validate actual external data
Static tools  → detect internal inconsistencies early
```

For your AI systems, type the stable internal interfaces strongly:

```
Protocol        → LLM providers, repositories, tools
TypedDict       → raw API-shaped payloads
dataclass       → validated domain objects
Literal         → model modes, statuses, categories
Generics        → reusable repositories and pipelines
Annotated       → validation or framework metadata
runtime checks  → external JSON and LLM output
```

Use one primary checker consistently, add it to CI, and let runtime validation protect the boundaries where data enters your system.[[typing.python](https://typing.python.org/en/latest/spec/generics.html)][[mypy.readthedocs](https://mypy.readthedocs.io/en/stable/generics.html)][[docs.astral](https://docs.astral.sh/ty/)]
