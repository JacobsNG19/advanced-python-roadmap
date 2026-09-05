# Advanced Object-Oriented Programming & Python's Object Model — Exercises

## Instructions

Solve each question independently. Choose your own implementation. The questions describe behavior and constraints but do not tell you which Python feature must be used.

---

## Exercise 1 — Human-readable and developer representations

Create a `Book` object with `title`, `author`, and `year`.

`str(book)` must produce:

```text
Python for AI Engineers — Toussaint Jacobs (2026)
```

`repr(book)` must include the class name and all three fields in an unambiguous form.

---

## Exercise 2 — Equality by identifier

Create a `Ticket` object with `ticket_id` and `title`.

Two tickets must compare equal when they have the same ID, even if their titles differ.

Tickets with different IDs must not compare equal.

Comparing a ticket with an unrelated type must not produce an incorrect ticket comparison.

---

## Exercise 3 — Hashable ticket keys

Create a `TicketKey` value object containing a ticket ID.

Requirements:

- Two keys with the same ID compare equal.
- Equal keys have equal hashes.
- A set removes duplicate logical keys.

```python
assert len({TicketKey("T-001"), TicketKey("T-001")}) == 1
```

---

## Exercise 4 — Vector operations

Create a two-dimensional vector with `x` and `y`.

Support:

```python
first + second
-first
abs(vector)
```

For `(3, 4)`, the absolute value must be `5`.

Unsupported operands must be handled appropriately.

---

## Exercise 5 — Collection object

Create `TicketCollection` containing ticket IDs.

It must support:

```python
len(collection)
collection[index]
for item in collection
item in collection
```

Repeated iteration over the collection must work.

---

## Exercise 6 — Callable classifier

Create an object that can be called like a function.

Its behavior must be:

```text
contains "payment"  → "billing"
contains "password" → "account_access"
otherwise            → "general"
```

---

## Exercise 7 — Managed resource

Create a session object usable with:

```python
with Session() as session:
    session.send("Hello")
```

The session must be active inside the block and inactive after the block.

---

## Exercise 8 — Validated temperature

Create a temperature object with a Celsius value.

Requirements:

- The value must be numeric.
- The value cannot be below `-273.15`.
- Reading the value must be possible through `temperature.celsius`.
- Assignment must be validated.

---

## Exercise 9 — Read-only balance

Create a bank account with a balance that can be read publicly but cannot be assigned directly.

Provide operations for depositing and withdrawing money.

Requirements:

- Deposits and withdrawals must be positive.
- Withdrawals cannot exceed the balance.
- Direct assignment to the public balance must fail.

---

## Exercise 10 — Reusable validated field

Create a reusable field mechanism for positive numeric values.

Use it for both:

```text
Subscription.monthly_price
Subscription.months
```

Both values must reject zero, negative numbers, and non-numeric values.

---

## Exercise 11 — Animal hierarchy

Create a general animal type and two specialized animal types.

Each specialized animal must provide its own sound.

The following loop must work:

```python
for animal in animals:
    print(animal.speak())
```

---

## Exercise 12 — Parent initialization

Create a `User` type with a username and an `AdminUser` type with permissions.

The specialized type must preserve the parent initialization and add its own data.

Its description must include both username and permissions.

---

## Exercise 13 — MRO experiment

Create classes `A`, `B`, `C`, and `D` such that `D` derives from both `B` and `C`, while `B` and `C` derive from `A`.

Give each class a method with the same name.

Determine and verify which implementation is selected for `D`.

Also expose the method-resolution order.

---

## Exercise 14 — Cooperative mixins

Create two independent capabilities:

```text
logging capability
validation capability
```

Combine them in a service type.

Both capabilities must initialize successfully through cooperative inheritance.

---

## Exercise 15 — Abstract repository

Define a repository contract requiring operations to:

```text
save an item
retrieve an item by ID
```

Create an in-memory implementation.

The contract itself must not be directly instantiable.

---

## Exercise 16 — Structural provider interface

Define an interface describing an object that can generate text from a prompt.

Create two unrelated implementations:

```text
LocalProvider
CloudProvider
```

A service must accept either implementation without changing its own code.

---

## Exercise 17 — Dataclass with validation

Create a `Product` data object with:

```text
name
price
```

Requirements:

- Strip whitespace from the name.
- Reject an empty name.
- Reject a negative price.
- Display useful object information when printed.

---

## Exercise 18 — Independent mutable fields

Create a `Project` data object with a task collection.

Two projects must not share the same task collection.

```python
first.tasks.append("Build MVP")
assert second.tasks == []
```

---

## Exercise 19 — Immutable value object

Create an immutable point with `x` and `y`.

Requirements:

- Fields cannot be reassigned after construction.
- Equal points compare equal.
- Equal points can be placed in a set as one logical value.

---

## Exercise 20 — Dataclass serialization

Create an experiment result object with:

```text
model_name
accuracy
samples
```

Convert it to JSON-compatible data and reconstruct an equivalent object from the serialized representation.

---

## Exercise 21 — Automatic subclass registry

Create a base plugin type that automatically records subclasses by a declared plugin name.

The following conceptual behavior must work:

```python
class SearchPlugin(Plugin, plugin_name="search"):
    ...

assert Plugin.registry["search"] is SearchPlugin
```

---

## Exercise 22 — Class registration system

Create a registration mechanism for plugin classes.

Register a class under a string name and retrieve the class later to instantiate it.

Duplicate names must be rejected.

---

## Exercise 23 — Metaclass validation

Create a class-creation rule requiring every concrete tool subclass to define a method named `run`.

A class that fails to define the method must be rejected when the class is created.

---

## Exercise 24 — Dynamic proxy

Create a proxy around another object.

The proxy must:

- Forward unknown attributes to the wrapped object.
- Print a message before calling a forwarded method.
- Return the original method result.

---

## Exercise 25 — Final typed ticket system

Build a ticket system containing:

- A ticket data object.
- A controlled status value.
- Equality based on ticket ID.
- A classifier interface.
- A concrete classifier.
- A service that receives the classifier from outside.

The service must classify a ticket without knowing the classifier’s concrete implementation.

Expected behavior:

```python
result = service.classify(ticket)
assert result == "billing"
```

# Practice rules

- Solve the questions in order.
- Add edge-case tests.
- Run a static checker on the typed exercises.
- Do not look at the solution file until you have attempted the problem.
