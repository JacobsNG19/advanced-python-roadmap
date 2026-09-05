# Performance, Internals & Optimization — Solutions

These solutions correspond to:

```text
Performance, Internals & Optimization - Exercises.md
```

---

## Exercise 1 — Establish a baseline

```python
from time import perf_counter


def process_titles(titles):
    return [title.strip().lower() for title in titles]


titles = ["  Ticket title  "] * 100_000

start = perf_counter()
result = process_titles(titles)
elapsed = perf_counter() - start

print(f"Elapsed: {elapsed:.6f} seconds")
print(f"Records: {len(result)}")
```

`perf_counter()` is appropriate for elapsed wall-clock measurements.

---

## Exercise 2 — `timeit` comparison

```python
import timeit


setup = "values = list(range(1000))"

comprehension_time = timeit.timeit(
    "[x * 2 for x in values]",
    setup=setup,
    number=10_000,
)

loop_time = timeit.timeit(
    """
result = []
for x in values:
    result.append(x * 2)
""",
    setup=setup,
    number=10_000,
)

print(comprehension_time)
print(loop_time)
```

Exact results depend on Python version and hardware. `timeit` reduces the effect of one-off timing noise by repeating the operation.

---

## Exercise 3 — `cProfile`

```python
import time


def load_data():
    return list(range(100_000))


def transform_data(values):
    time.sleep(0.2)
    return [value * 2 for value in values]


def save_data(values):
    return len(values)


def main():
    values = load_data()
    transformed = transform_data(values)
    save_data(transformed)


if __name__ == "__main__":
    main()
```

Run:

```bash
python -m cProfile -s cumulative app.py
```

`transform_data()` should dominate cumulative time because it includes the deliberate delay.

---

## Exercise 4 — `pstats`

```python
import cProfile
import pstats


profiler = cProfile.Profile()
profiler.enable()

main()

profiler.disable()
profiler.dump_stats("profile.prof")

stats = pstats.Stats("profile.prof")
stats.strip_dirs()
stats.sort_stats("cumulative")
stats.print_stats(10)
stats.print_callers(10)
```

`cumulative` includes time spent in called functions. `tottime` measures time spent inside the function itself.

---

## Exercise 5 — Memory snapshot

```python
import tracemalloc


tracemalloc.start()

before = tracemalloc.take_snapshot()

values = [
    "ticket-" + str(number)
    for number in range(100_000)
]

after = tracemalloc.take_snapshot()

for stat in after.compare_to(
    before,
    "lineno",
)[:10]:
    print(stat)
```

The comparison identifies source lines whose allocations increased between snapshots.

---

## Exercise 6 — Peak memory

```python
import tracemalloc


def list_version(limit):
    return sum([
        number * number
        for number in range(limit)
    ])


def lazy_version(limit):
    return sum(
        number * number
        for number in range(limit)
    )


def measure(function, limit):
    tracemalloc.start()
    tracemalloc.reset_peak()

    result = function(limit)
    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return result, current, peak


list_result = measure(list_version, 1_000_000)
lazy_result = measure(lazy_version, 1_000_000)

assert list_result[0] == lazy_result[0]
print("List peak:", list_result[2])
print("Lazy peak:", lazy_result[2])
```

The lazy version generally has a lower peak Python allocation because it does not retain the intermediate list.

---

## Exercise 7 — Reference behavior

```python
values = [1, 2]
alias = values

alias.append(3)

assert values == [1, 2, 3]
assert alias is values

copy = values.copy()
copy.append(4)

assert values == [1, 2, 3]
assert copy == [1, 2, 3, 4]
assert copy is not values
```

Assignment creates another reference; `.copy()` creates a shallow copy.

---

## Exercise 8 — Cyclic references

```python
import gc


class Node:
    pass


first = Node()
second = Node()

first.other = second
second.other = first

first_id = id(first)
second_id = id(second)

del first
del second

collected = gc.collect()

print(f"Collected objects: {collected}")
```

The garbage collector can find unreachable cycles that reference counting alone cannot immediately remove.

---

## Exercise 9 — `gc` inspection

```python
import gc


print("Enabled:", gc.isenabled())
print("Counts:", gc.get_count())
print("Thresholds:", gc.get_threshold())

collected = gc.collect()
print("Collected:", collected)
```

Do not call `gc.collect()` repeatedly in hot loops without evidence that it helps.

---

## Exercise 10 — Compare instance memory

```python
import tracemalloc


class NormalPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SlottedPoint:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


def measure(cls, count):
    tracemalloc.start()

    points = [
        cls(index, index)
        for index in range(count)
    ]

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return points, current, peak


normal_points, _, normal_peak = measure(
    NormalPoint,
    100_000,
)

slotted_points, _, slotted_peak = measure(
    SlottedPoint,
    100_000,
)

print(normal_peak)
print(slotted_peak)

try:
    slotted_points[0].z = 10
except AttributeError:
    rejected = True
else:
    rejected = False

assert rejected is True
```

Measure on your own interpreter. `__slots__` is useful only when its memory and design benefits justify its restrictions.

---

## Exercise 11 — Weak references

```python
import weakref


class Model:
    pass


model = Model()
reference = weakref.ref(model)

assert reference() is model

del model

assert reference() is None
```

The weak reference does not keep the object alive.

---

## Exercise 12 — Weak-value cache

```python
from weakref import WeakValueDictionary


class Model:
    def __init__(self, name):
        self.name = name


cache = WeakValueDictionary()
model = Model("classifier-v1")
cache["classifier"] = model

assert cache["classifier"].name == "classifier-v1"

del model

assert "classifier" not in cache
```

The cache entry disappears when the object has no strong references.

---

## Exercise 13 — Algorithmic improvement

```python
from time import perf_counter


categories = [f"category-{i}" for i in range(100_000)]
category_set = set(categories)
queries = ["category-99999"] * 10_000

start = perf_counter()
list_results = [query in categories for query in queries]
list_time = perf_counter() - start

start = perf_counter()
set_results = [query in category_set for query in queries]
set_time = perf_counter() - start

assert list_results == set_results
print("List:", list_time)
print("Set:", set_time)
```

A set is generally more appropriate for repeated membership testing.

---

## Exercise 14 — Avoid intermediate collections

```python
import tracemalloc


def list_version(limit):
    return sum([
        number * number
        for number in range(limit)
    ])


def generator_version(limit):
    return sum(
        number * number
        for number in range(limit)
    )


def measure(function, limit):
    tracemalloc.start()
    tracemalloc.reset_peak()

    result = function(limit)
    _, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()
    return result, peak


list_result, list_peak = measure(
    list_version,
    1_000_000,
)

generator_result, generator_peak = measure(
    generator_version,
    1_000_000,
)

assert list_result == generator_result
print(list_peak)
print(generator_peak)
```

The generator version usually lowers peak memory usage.

---

## Exercise 15 — Caching

```python
from functools import lru_cache
from time import sleep


@lru_cache(maxsize=128)
def expensive_lookup(value):
    sleep(0.05)
    return value * value


first = expensive_lookup(10)
second = expensive_lookup(10)

assert first == second == 100
print(expensive_lookup.cache_info())

expensive_lookup.cache_clear()
```

Caching is appropriate here because the function is deterministic and has no externally visible side effects.

---

## Exercise 16 — Threading and the GIL experiment

```python
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
)
from time import perf_counter


def cpu_work(limit):
    total = 0

    for number in range(limit):
        total += number * number

    return total


def sequential(values):
    return [cpu_work(value) for value in values]


def threaded(values):
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(cpu_work, values))


def processed(values):
    with ProcessPoolExecutor(max_workers=4) as executor:
        return list(executor.map(cpu_work, values))


def measure(function, values):
    start = perf_counter()
    result = function(values)
    elapsed = perf_counter() - start
    return result, elapsed


if __name__ == "__main__":
    values = [2_000_000] * 4

    sequential_result, sequential_time = measure(
        sequential,
        values,
    )

    threaded_result, threaded_time = measure(
        threaded,
        values,
    )

    process_result, process_time = measure(
        processed,
        values,
    )

    assert sequential_result == threaded_result
    assert sequential_result == process_result

    print(sequential_time)
    print(threaded_time)
    print(process_time)
```

The process version may use multiple cores. Threads may not improve pure-Python CPU work under the normal GIL build.

---

## Exercise 17 — Free-threading investigation

```python
import sysconfig


gil_disabled = sysconfig.get_config_var(
    "Py_GIL_DISABLED"
)

if gil_disabled:
    print("Interpreter supports free-threading.")
else:
    print("Interpreter is not a free-threaded build.")
```

Support for free-threaded CPython builds exists in recent Python versions, but the build and installed extension compatibility must still be verified.

---

## Exercise 18 — Optimize only after profiling

Original version:

```python
def classify_slow(tickets):
    results = []

    for ticket in tickets:
        text = ticket["text"].lower()

        categories = [
            "payment",
            "password",
            "error",
        ]

        if any(
            keyword in text
            for keyword in categories
        ):
            category = "support"
        else:
            category = "general"

        results.append({
            "id": ticket["id"],
            "category": category,
        })

    return results
```

Improved version:

```python
KEYWORDS = {
    "payment",
    "password",
    "error",
}


def classify_fast(tickets):
    results = []

    for ticket in tickets:
        text = ticket["text"].lower()
        category = (
            "support"
            if any(
                keyword in text
                for keyword in KEYWORDS
            )
            else "general"
        )

        results.append({
            "id": ticket["id"],
            "category": category,
        })

    return results
```

The improvement moves invariant configuration outside the loop. Profile both versions and verify equal output before claiming a speedup.

---

## Exercise 19 — Native acceleration experiment

A vectorized NumPy version:

```python
import numpy as np


def python_squares(values):
    return [value * value for value in values]


def numpy_squares(values):
    array = np.asarray(values)
    return array * array


values = list(range(100_000))

python_result = python_squares(values)
numpy_result = numpy_squares(values)

assert np.array_equal(
    python_result,
    numpy_result,
)
```

For numerical arrays, vectorized native operations may outperform Python loops. Benchmark with your real workload.

---

## Exercise 20 — Final optimization report

Example report structure:

```text
Function:
    process_tickets

Baseline:
    0.82 seconds for 1,000,000 records

Profiling result:
    Repeated construction of a keyword collection inside the loop

Change:
    Move the invariant collection outside the loop

Correctness:
    Old and new outputs compared equal for normal and edge cases

New measurement:
    0.54 seconds for the same input

Speedup:
    0.82 / 0.54 ≈ 1.52x

Memory:
    Peak allocation remained approximately unchanged

Decision:
    Keep the optimization because it is small, readable, and reduces
    repeated work without adding significant complexity.
```

The exact measurements must come from your own machine and workload.

---

# Review checklist

You should now understand:

- The difference between timing and profiling.
- How to use `cProfile` and `pstats`.
- How `tracemalloc` compares memory snapshots.
- Python names, references, identity, and copying.
- Reference counting and cyclic garbage collection.
- The purpose and limitations of `__slots__`.
- How weak references support non-owning caches.
- Why algorithmic improvements usually matter most.
- Why generators can reduce peak memory.
- Why caching requires deterministic behavior.
- How the GIL affects CPU-bound Python threads.
- Why processes help with CPU-bound work.
- What free-threaded builds change.
- When NumPy, Numba, Cython, or C extensions may be appropriate.
