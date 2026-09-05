# Iterators, Generators & Context Managers — Exercises

## Instructions

Solve each question independently. Choose your own implementation. The questions describe required behavior but do not prescribe a particular technique.

---

## Exercise 1 — Consume a sequence

Given:

```python
values = [10, 20, 30]
```

Read the values one at a time and detect when there are no more values.

Expected values:

```text
10
20
30
```

---

## Exercise 2 — Countdown

Create `Countdown(start)`.

Its values must begin at `start` and continue down to `0`.

```python
assert list(Countdown(3)) == [3, 2, 1, 0]
```

---

## Exercise 3 — Step sequence

Create `StepSequence(start, stop, step)`.

Produce values beginning at `start`, stopping before `stop`, and changing by `step`.

```python
assert list(StepSequence(0, 10, 2)) == [0, 2, 4, 6, 8]
assert list(StepSequence(5, 0, -2)) == [5, 3, 1]
```

A step of zero must be rejected.

---

## Exercise 4 — Reusable collection

Create `TicketCollection` containing ticket IDs.

The collection must:

- Support repeated iteration.
- Support `len(collection)`.
- Support `collection[index]`.

```python
collection = TicketCollection(["T-001", "T-002"])

assert list(collection) == ["T-001", "T-002"]
assert list(collection) == ["T-001", "T-002"]
assert len(collection) == 2
assert collection[0] == "T-001"
```

---

## Exercise 5 — Positive values

Create `positive_values(values)` that produces only values greater than zero.

```python
assert list(positive_values([-2, 0, 3, -1, 5])) == [3, 5]
```

---

## Exercise 6 — Even numbers

Create `even_numbers(limit)` that produces even numbers from `0` through `limit`.

```python
assert list(even_numbers(10)) == [0, 2, 4, 6, 8, 10]
```

---

## Exercise 7 — Squares

Create a lazy sequence of the squares from `0` through `9`.

```python
assert list(squares()) == [
    0, 1, 4, 9, 16,
    25, 36, 49, 64, 81,
]
```

---

## Exercise 8 — Non-empty file lines

Create `non_empty_lines(path)`.

It must read a text file, remove surrounding whitespace, ignore blank lines, and produce the remaining lines one at a time.

For a file containing:

```text
 First line

 Second line
```

expected output:

```python
["First line", "Second line"]
```

---

## Exercise 9 — Text processing pipeline

Create `process_text(values)` that:

1. Removes surrounding whitespace.
2. Ignores empty values.
3. Converts remaining values to lowercase.

```python
assert list(process_text([
    "  Python  ",
    "",
    "  AI  ",
])) == ["python", "ai"]
```

---

## Exercise 10 — Flatten batches

Create `flatten(batches)`.

```python
batches = [
    ["T-001", "T-002"],
    ["T-003"],
    ["T-004", "T-005"],
]

assert list(flatten(batches)) == [
    "T-001",
    "T-002",
    "T-003",
    "T-004",
    "T-005",
]
```

---

## Exercise 11 — Stream with a final total

Create `values_with_total(values)`.

It must produce every input value and make the final total available when the sequence finishes.

For `[1, 2, 3]`, the produced values must be `1`, `2`, and `3`, and the final total must be `6`.

---

## Exercise 12 — Resource session

Create a `Session` resource that can be used like this:

```python
with Session() as session:
    assert session.send("hello") == "Sent: hello"
```

The session must be active inside the block and inactive after the block.

---

## Exercise 13 — Cleanup after success and failure

Create a resource that records whether cleanup happened.

Verify that cleanup happens when:

1. The block completes normally.
2. The block raises an exception.

The exception must not be hidden.

---

## Exercise 14 — Suppress one exception type

Create a resource that suppresses `ValueError` but does not suppress `TypeError`.

```python
with YourResource():
    raise ValueError("ignored")
```

The program must continue after the first block.

---

## Exercise 15 — Timer resource

Create `Timer(label)`.

It must report the elapsed time after the block finishes, including when the block raises an exception.

---

## Exercise 16 — Temporary setting

Create `temporary_setting(settings, key, value)`.

Inside the block, the setting must have the temporary value. After the block, the previous state must be restored.

Test both cases:

- The key existed before the block.
- The key did not exist before the block.

---

## Exercise 17 — Managed text file

Create a resource that opens a text file on entry and closes it on exit.

Use it like this:

```python
with ManagedFile("notes.txt", "w") as file:
    file.write("Python")
```

After the block, the file must be closed.

---

## Exercise 18 — Dynamic file reading

Given a list of file paths, read all files safely and return their contents.

The number of files is not fixed in advance.

```python
assert read_files([first, second]) == ["A", "B"]
```

---

## Exercise 19 — Async session

Create an asynchronous session usable like this:

```python
async with AsyncSession() as session:
    result = await session.fetch("resource")
```

The session must open before the block and close afterward.

---

## Exercise 20 — Async event stream

Create an asynchronous event source that produces:

```text
ticket.created
ticket.classified
ticket.closed
```

with a small pause between events.

Consume it and verify the event order.

---

## Exercise 21 — Final streaming pipeline

Build a complete pipeline that:

1. Receives raw ticket dictionaries.
2. Normalizes their text.
3. Keeps only high-priority tickets.
4. Produces only ticket IDs.
5. Measures execution time with a managed timer.

Expected result:

```python
[
    "T-001",
    "T-003",
]
```

# Practice rules

- Solve the questions in order.
- Do not look at the solution file until you have attempted the problem.
- Add at least one edge-case test for every exercise.
- Check that lazy sequences are not unnecessarily converted into lists.
- Check that resources are cleaned up when exceptions occur.
