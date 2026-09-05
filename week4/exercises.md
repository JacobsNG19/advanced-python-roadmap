# Modern Type System & Static Typing — Exercises

## Instructions

Solve each question independently. Choose your own implementation. The questions describe expected behavior without prescribing a particular technique.

Use a static checker while working:

```bash
mypy .
pyright
# or: uvx ty check
```

---

## Exercise 1 — Annotated function

Annotate `add()` so it accepts two integers and returns an integer.

```python
def add(first, second):
    return first + second
```

The checker should identify calls that pass incompatible arguments.

---

## Exercise 2 — Optional result

Create a typed `find_user(username)` function that returns a user record when found and `None` otherwise.

A user record must contain:

```text
id: str
username: str
```

---

## Exercise 3 — Union narrowing

Create `format_value(value)` for a value that may be an integer or a string.

Expected behavior:

```python
format_value(10)       # "Integer: 10"
format_value("hello")  # "Text: HELLO"
```

---

## Exercise 4 — Unknown input

Create `display(value)` that accepts an unknown value and safely returns its string representation.

Do not assume that the value has string-specific methods until you establish its type.

---

## Exercise 5 — Generic first item

Create a function that accepts a list of any one item type and returns its first item while preserving the item type in the annotation.

It must reject an empty list.

---

## Exercise 6 — Generic box

Create a reusable container that stores a value and provides operations to read and replace it.

The type of the replacement must match the type used to create the container.

---

## Exercise 7 — Generic repository

Create a repository that is parameterized by:

```text
entity type
ID type
```

It must support saving and retrieving entities by ID.

---

## Exercise 8 — Typed ticket dictionary

Describe this dictionary structure using static types:

```python
{
    "id": "T-001",
    "title": "Cannot log in",
    "priority": "high",
}
```

All three keys must be required.

---

## Exercise 9 — Allowed literal values

Define the allowed ticket priorities as:

```text
low
normal
high
```

Use the type in a ticket structure and in a ticket-creation function.

---

## Exercise 10 — Optional dictionary key

Create a typed user structure with required fields:

```text
username
email
```

and an optional field:

```text
phone
```

The `phone` key itself may be absent.

---

## Exercise 11 — Tagged response union

Create two response structures:

```text
success → status="success", data
error   → status="error", message
```

Create a function that handles both responses by examining the status.

---

## Exercise 12 — Protocol for notifications

Describe an object that can send a message and return a string.

Create two unrelated implementations:

```text
EmailNotifier
SMSNotifier
```

Create a function that works with either one.

---

## Exercise 13 — Protocol with attributes

Describe an AI model provider that has:

```text
name: str
generate(prompt: str) -> str
```

Create a compatible local provider.

---

## Exercise 14 — Generic protocol

Describe a transformer that maps an input type to an output type.

Create a transformer that maps strings to integers by returning string length.

---

## Exercise 15 — Annotated metadata

Create an annotated username type containing metadata that describes a minimum length of three characters.

Inspect the annotation metadata at runtime.

---

## Exercise 16 — Runtime input validation

Create `parse_ticket(data)` for unknown external data.

It must return a valid typed ticket only when:

- `data` is a dictionary.
- `id` is a string.
- `title` is a string.
- `priority` is one of the allowed values.

Otherwise it must raise an appropriate exception.

---

## Exercise 17 — Custom type narrowing

Create a predicate that determines whether a list of unknown objects contains only strings.

The static checker should understand that the list contains strings inside a successful conditional branch.

---

## Exercise 18 — Distinct IDs

Create distinct static types for `UserID` and `TicketID`, even though both use strings at runtime.

Create a function that accepts only `TicketID`.

---

## Exercise 19 — Immutable constant and class field

Declare:

```text
MAX_RETRIES as a non-reassignable integer constant
User.platform as a class variable
```

---

## Exercise 20 — Fluent API

Create a query object whose methods return the current object so calls can be chained.

The return annotation must preserve the concrete class type.

```python
query.where("priority = 'high'").limit(10)
```

---

## Exercise 21 — Overloaded function

Create a function with these input/output relationships:

```text
int  → int
str  → str
```

For strings, remove surrounding whitespace. For integers, return the value unchanged.

---

## Exercise 22 — Typed decorator

Create a decorator that logs a function call while preserving the wrapped function's parameter and return types for static analysis.

---

## Exercise 23 — Typed model result

Create a frozen dataclass containing:

```text
category: one of billing, account_access, technical, general
confidence: float between 0 and 1
```

Validate the confidence at runtime.

---

## Exercise 24 — Static checker configuration

Create a `pyproject.toml` configuration for:

```text
pytest
Ruff
Pyright
```

Configure source and test directories for Pyright.

---

## Exercise 25 — Final typed AI service

Build a small typed ticket-classification service containing:

- A classifier interface.
- A concrete classifier.
- A frozen classification-result object.
- A service that receives the classifier from outside.
- Runtime validation for empty text.
- A fake classifier suitable for testing.

The service must classify payment-related text as `billing`.

# Practice rules

- Solve the questions in order.
- Run a type checker after every few exercises.
- Add edge-case tests.
- Do not use `cast()` as a replacement for runtime validation.
- Do not look at the solutions until you have attempted the problem.
