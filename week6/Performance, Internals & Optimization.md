Performance work should follow this order:

```
Measure → identify the bottleneck → change one thing → measure again
```

Do not optimize based only on intuition. Python provides deterministic profilers such as `cProfile`, memory tracing with `tracemalloc`, garbage-collector controls, `__slots__`, weak references, and several options for CPU parallelism.[[docs.python](https://docs.python.org/3/library/tracemalloc.html)][[docs.python](https://docs.python.org/3/library/gc.html)][[docs.python](https://docs.python.org/3/library/profile.html)]

# 1. What are you optimizing?

There are several different performance problems:

|Problem|Typical tool|
|---|---|
|Which functions consume CPU time?|`cProfile`, `pstats`, `py-spy`, Scalene|
|Which lines allocate memory?|`tracemalloc`, Scalene|
|Too many objects or retained references|`gc`, `weakref`|
|Excessive per-object memory|`__slots__`|
|CPU-bound pure Python|Multiprocessing or process pools|
|Numerical loops|NumPy, Numba, Cython|
|Blocking I/O|Asyncio or threads|
|Slow algorithms|Better algorithm/data structure|

A faster function does not help if the real bottleneck is:

- A database query.
- A network request.
- Excessive serialization.
- An inefficient algorithm.
- A memory leak.
- Repeated model/API calls.

# 2. Start with a baseline

Before optimizing, measure the current version.

```
from time import perf_counter


def process_tickets(tickets):
    return [
        ticket.strip().lower()
        for ticket in tickets
    ]


tickets = [
    "Cannot log in",
    "Payment failed",
] * 100_000

start = perf_counter()

result = process_tickets(tickets)

elapsed = perf_counter() - start

print(f"{elapsed:.4f} seconds")
```

This is useful for a quick measurement, but it is not a complete benchmark.

For repeatable microbenchmarks, use:

```
python -m timeit \
    -s "data = list(range(1000))" \
    "[x * 2 for x in data]"
```

`cProfile` is for finding where a program spends time; it is not primarily a precise benchmarking tool. The Python documentation recommends benchmark tools such as `timeit` for reasonably accurate timing and profilers for execution profiles.[[docs.python](https://docs.python.org/3/library/profile.html)]

# 3. `cProfile`

`cProfile` is Python’s standard deterministic profiler and is implemented as a C extension with reasonable overhead.[[docs.python](https://docs.python.org/3/library/profile.html)]

Profile a script:

```
python -m cProfile app.py
```

Sort by cumulative time:

```
python -m cProfile -s cumulative app.py
```

Save results:

```
python -m cProfile -o profile.prof app.py
```

The most useful sorting choices include:

```
cumulative → total time including called functions
tottime    → time inside the function itself
calls      → number of calls
```

## Profile a function

```
import cProfile


def expensive_work():
    values = []

    for number in range(1_000_000):
        values.append(number * number)

    return sum(values)


cProfile.run("expensive_work()")
```

For better control:

```
import cProfile
import pstats


profiler = cProfile.Profile()

profiler.enable()

expensive_work()

profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(10)
```

This prints the ten most important functions.

## Reading the output

Typical columns:

```
ncalls  → number of calls
tottime → time inside function
percall → time per call
cumtime → cumulative time including subcalls
filename:lineno(function) → source location
```

If a function has:

```
tottime = high
```

its own implementation is slow.

If it has:

```
cumtime = high
tottime = low
```

one of the functions it calls is probably the bottleneck.

# 4. `pstats`

Read a saved profile:

```
import pstats


stats = pstats.Stats("profile.prof")

stats.strip_dirs()
stats.sort_stats("cumulative")
stats.print_stats(20)
```

Useful operations:

```
stats.print_callers()
stats.print_callees()
```

- `print_callers()` shows who called a function.
- `print_callees()` shows what a function called.

The workflow is:

```
python -m cProfile -o profile.prof app.py
        ↓
load profile.prof with pstats
        ↓
sort by cumulative time
        ↓
inspect the hottest functions
```

# 5. `py-spy`

`py-spy` is an external sampling profiler that can inspect a running Python process with minimal code changes.

Install:

```
python -m pip install py-spy
```

Run a script:

```
py-spy record -o profile.svg -- python app.py
```

View:

```
profile.svg
```

It produces a flame graph showing where execution time is spent.

Attach to a running process:

```
py-spy top --pid 12345
```

Use `py-spy` when:

- You cannot easily modify the application.
- The program is long-running.
- You want production-like observation.
- You want low-overhead sampling.
- You need to inspect a live process.

## `cProfile` versus `py-spy`

|Tool|Style|Best use|
|---|---|---|
|`cProfile`|Deterministic instrumentation|Detailed function-level local profiling|
|`py-spy`|Sampling profiler|Live processes and low-intrusion observation|

# 6. Scalene

Scalene is an external profiler that can report:

- CPU time.
- Python time.
- Native time.
- Memory allocation.
- Line-level behavior.
- Copying and memory usage in some cases.

Install:

```
python -m pip install scalene
```

Run:

```
scalene app.py
```

Use Scalene when you want line-level information and a combined view of CPU and memory behavior.

A practical tool sequence is:

```
cProfile → identify slow functions
py-spy    → inspect live application behavior
Scalene   → investigate CPU and memory by line
```

# 7. Memory profiling with `tracemalloc`

`tracemalloc` traces memory blocks allocated by Python and can report allocation locations, statistics, and differences between snapshots.[[docs.python](https://docs.python.org/3/library/tracemalloc.html)]

Basic usage:

```
import tracemalloc


tracemalloc.start()

snapshot_before = tracemalloc.take_snapshot()

data = [
    "ticket" * 100
    for _ in range(100_000)
]

snapshot_after = tracemalloc.take_snapshot()

differences = snapshot_after.compare_to(
    snapshot_before,
    "lineno",
)

for difference in differences[:10]:
    print(difference)
```

This helps identify which lines caused memory growth.

## Current and peak memory

```
import tracemalloc


tracemalloc.start()

data = [
    number * number
    for number in range(100_000)
]

current, peak = (
    tracemalloc.get_traced_memory()
)

print(f"Current: {current / 1024:.2f} KiB")
print(f"Peak: {peak / 1024:.2f} KiB")
```

Reset peak measurement:

```
tracemalloc.reset_peak()
```

Stop tracing:

```
tracemalloc.stop()
```

Start tracing early if you want to observe allocations from the beginning of the program.[[docs.python](https://docs.python.org/3/library/tracemalloc.html)]

## Snapshot by filename

```
snapshot = tracemalloc.take_snapshot()

for stat in snapshot.statistics("filename")[:10]:
    print(stat)
```

Other grouping options:

```
"lineno"
"filename"
"traceback"
```

Use:

```
lineno    → exact source lines
filename  → files
traceback → allocation call paths
```

# 8. Finding memory leaks

A memory leak in Python often means objects remain reachable through references even though the application no longer needs them.

Take snapshots at different points:

```
import tracemalloc


tracemalloc.start()

snapshot_one = tracemalloc.take_snapshot()

for _ in range(10):
    process_batch()

snapshot_two = tracemalloc.take_snapshot()

for stat in snapshot_two.compare_to(
    snapshot_one,
    "lineno",
)[:10]:
    print(stat)
```

Look for:

- A collection that grows forever.
- A cache without an eviction policy.
- Global references.
- Callbacks retaining objects.
- Closures retaining large values.
- Task references that are never released.
- Event listeners never removed.

`tracemalloc` traces Python-managed allocations. It may not show every allocation made by native extensions or external processes.

# 9. Python’s memory model

Python variables are names bound to objects.

```
a = [1, 2, 3]
b = a
```

Both names refer to the same list:

```
b.append(4)

print(a)
```

Output:

```
[1, 2, 3, 4]
```

There is one list and two references.

## Assignment does not copy

```
first = {"value": 10}
second = first

second["value"] = 20

print(first)
```

Output:

```
{'value': 20}
```

Create a shallow copy:

```
second = first.copy()
```

For nested structures:

```
from copy import deepcopy


second = deepcopy(first)
```

## Object identity

```
a = []
b = a
c = []

print(a is b)
print(a is c)
print(a == c)
```

Output:

```
True
False
True
```

- `is` checks object identity.
- `==` checks logical equality.

Use:

```
value is None
```

not:

```
value == None
```

# 10. Reference counting and garbage collection

CPython primarily uses reference counting.

```
import sys


value = []

print(sys.getrefcount(value))
```

The exact count includes temporary references created by the function call, so do not treat it as a precise application metric.

When an object has no remaining references, it can usually be destroyed immediately.

But reference cycles require cyclic garbage collection:

```
class Node:
    pass


first = Node()
second = Node()

first.other = second
second.other = first

del first
del second
```

The objects refer to each other, forming a cycle.

Python’s cyclic garbage collector can detect unreachable cycles. The `gc` module provides controls for inspecting, enabling, disabling, and debugging garbage collection.[[docs.python](https://docs.python.org/3/library/gc.html)]

## Inspect garbage collection

```
import gc


print(gc.isenabled())
print(gc.get_count())
print(gc.get_threshold())
```

Collect manually:

```
collected = gc.collect()

print(collected)
```

Do not call `gc.collect()` repeatedly in performance-critical loops without measuring. Collection itself has a cost.

## Debug unreachable objects

```
import gc


gc.set_debug(gc.DEBUG_SAVEALL)

gc.collect()

print(gc.garbage)
```

`DEBUG_SAVEALL` saves unreachable objects in `gc.garbage` instead of freeing them, which can help inspect leaks.[[docs.python](https://docs.python.org/3/library/gc.html)]

# 11. `__del__` and garbage collection

Avoid relying on:

```
def __del__(self):
    ...
```

for important cleanup.

Problems include:

- Unpredictable timing.
- Complicated reference cycles.
- Interpreter shutdown behavior.
- Exceptions during finalization.
- Partially destroyed module state.

Prefer:

```
with resource:
    ...
```

or:

```
resource.close()
```

Context managers are much more reliable for files, connections, locks, and transactions.

# 12. `__slots__`

Normal Python instances usually have a dynamic `__dict__` storing attributes.

```
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

With `__slots__`, you define permitted instance attributes:

```
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

This prevents arbitrary new attributes:

```
point = Point(1, 2)

point.z = 3
```

Output:

```
AttributeError
```

## Why use `__slots__`?

Potential benefits:

- Lower memory use for many small objects.
- Faster attribute access in some cases.
- Preventing accidental attributes.
- More predictable object layout.

The Python documentation explains that slots are implemented at the class level through descriptors.[[docs.python](https://docs.python.org/3/reference/datamodel.html?highlight=setattr)]

## Limitations

Instances with `__slots__` normally do not have:

```
__dict__
```

So this may fail:

```
point.__dict__
```

They may also not support weak references unless you include:

```
"__weakref__"
```

Multiple inheritance with slots requires care.

## Do not use blindly

Use `__slots__` when:

- You have measured memory pressure.
- You create very many small objects.
- The object shape is intentionally fixed.

Do not add it just because it sounds faster.

Dataclasses support slots:

```
from dataclasses import dataclass


@dataclass(slots=True)
class Point:
    x: float
    y: float
```

# 13. Weak references

A normal reference keeps an object alive:

```
cache = {}

object_key = SomeObject()
cache["item"] = object_key
```

As long as `cache` contains the object, it remains reachable.

A **weak reference** does not keep the object alive. When no strong references remain, the object can be collected.

```
import weakref
```

```
class Model:
    pass


model = Model()
reference = weakref.ref(model)

print(reference())
```

Output resembles:

```
<__main__.Model object at 0x...>
```

Delete the strong reference:

```
del model

print(reference())
```

Output:

```
None
```

## Weak-value dictionary

```
from weakref import WeakValueDictionary


class Model:
    def __init__(self, name):
        self.name = name


cache = WeakValueDictionary()

model = Model("classifier-v1")
cache["classifier"] = model

print(cache["classifier"].name)

del model
```

Once the object has no strong references, it can disappear from the weak-value dictionary.

Use weak references for:

- Caches.
- Object registries.
- Parent-child relationships.
- Observers.
- Event listeners.
- Metadata associated with object lifetimes.

The `weakref` documentation notes that weak references allow access without keeping the referent alive. It also notes that slots-based classes need `__weakref__` to support weak references.[[docs.python](https://docs.python.org/3/library/weakref.html)]

## Weak-key dictionary

```
from weakref import WeakKeyDictionary


class User:
    pass


metadata = WeakKeyDictionary()

user = User()
metadata[user] = {
    "last_seen": "today",
}

del user
```

When the key object disappears, its metadata can disappear too.

# 14. The GIL in practice

In standard CPython builds, the GIL limits multiple threads from executing Python bytecode simultaneously.

CPU-bound threaded example:

```
def cpu_work():
    total = 0

    for number in range(20_000_000):
        total += number * number

    return total
```

Adding threads may not provide true CPU parallelism for this pure-Python loop.

I/O-bound example:

```
import time


def io_work():
    time.sleep(2)
```

Threads can overlap the waiting:

```
from concurrent.futures import ThreadPoolExecutor


with ThreadPoolExecutor(
    max_workers=4
) as executor:
    list(
        executor.map(
            lambda _: io_work(),
            range(4),
        )
    )
```

Approximate duration:

```
2 seconds
```

rather than:

```
8 seconds
```

The GIL does not prevent useful concurrency; it mainly affects CPU-bound Python bytecode.

# 15. Free-threaded Python

Starting with CPython 3.13, Python supports optional free-threaded builds in which the GIL is disabled. These can allow threads to execute Python code in parallel on multiple CPU cores.[[docs.python](https://docs.python.org/3/howto/free-threading-python.html)]

Important caveats:

- Free-threaded builds are not the default.
- Not every package supports them equally.
- Some C extensions may cause the GIL to be enabled again.
- Thread safety still matters.
- Built-in operations should not be treated as a substitute for correct synchronization.
- Performance gains depend on the workload.
- Compatibility must be tested.

Check whether the interpreter supports free-threading:

```
import sysconfig


gil_disabled_support = sysconfig.get_config_var(
    "Py_GIL_DISABLED"
)

print(gil_disabled_support)
```

The Python documentation identifies `Py_GIL_DISABLED` as the recommended configuration check for whether the interpreter supports free-threading.[[docs.python](https://docs.python.org/3/howto/free-threading-python.html)]

Free-threaded Python changes the performance landscape, but it does not remove the need for:

```
locks
queues
careful shared-state design
```

# 16. Common optimization techniques

## Improve the algorithm

This is usually the highest-impact optimization.

Slow membership check:

```
allowed = ["billing", "general", "technical"]

if category in allowed:
    ...
```

For frequent membership tests:

```
allowed = {
    "billing",
    "general",
    "technical",
}
```

Set lookup is generally more appropriate.

## Avoid repeated work

Bad:

```
for ticket in tickets:
    normalized = ticket.text.lower()

    if ticket.text.lower() == normalized:
        ...
```

Better:

```
for ticket in tickets:
    normalized = ticket.text.lower()

    if normalized == ticket.expected:
        ...
```

## Use local references carefully

In extremely hot loops, local lookups can matter:

```
append = results.append

for item in items:
    append(transform(item))
```

But do this only after profiling; it can make code less readable.

## Use built-ins

Built-ins are often implemented in optimized C:

```
sum(values)
any(values)
all(values)
sorted(values)
```

Prefer:

```
total = sum(values)
```

over a manual Python loop when the behavior is equivalent.

## Avoid unnecessary copies

Bad:

```
for item in list(items):
    ...
```

if you do not need a copy.

Bad:

```
result = list(
    transform(item)
    for item in items
)
```

if the consumer can use a generator directly:

```
result = sum(
    transform(item)
    for item in items
)
```

## Use generators for large streams

```
def read_records(records):
    for record in records:
        yield transform(record)
```

This avoids holding every intermediate result in memory.

## Batch operations

Instead of making one database/API call per item:

```
for ticket in tickets:
    save_ticket(ticket)
```

prefer a batch operation where supported:

```
save_tickets(tickets)
```

This often reduces:

- Network round trips.
- Serialization overhead.
- Database transaction overhead.
- Connection setup cost.

## Cache carefully

```
from functools import lru_cache


@lru_cache(maxsize=128)
def parse_config(path):
    ...
```

Only cache deterministic results whose invalidation behavior you understand.

## Use appropriate data structures

```
set       → membership
dict      → key lookup
deque     → queue/front removal
heapq     → priority queue
Counter   → frequency counting
generator → lazy stream
```

# 17. CPU optimization options

## Vectorized libraries

For numerical work, use NumPy or another optimized library where appropriate:

```
import numpy as np


values = np.arange(1_000_000)
squared = values * values
```

The loop runs in optimized native code rather than ordinary Python bytecode.

## Numba

Numba can compile suitable numerical Python functions.

```
python -m pip install numba
```

Example:

```
from numba import njit


@njit
def sum_squares(values):
    total = 0

    for value in values:
        total += value * value

    return total
```

Numba works best with supported numerical Python patterns and array-oriented workloads. It is not a universal accelerator for arbitrary Python code.

## Cython

Cython lets you write Python-like code with optional static types and compile it into extension modules.

Use it when:

- A hot loop is clearly identified.
- You need C-level performance.
- The code is stable enough to compile.
- Numba or vectorization is not a good fit.

Cython adds build complexity, so do not use it before profiling.

## C extensions

Writing a C extension can provide maximum control and performance, but it is the most complex option:

- C API details.
- Reference counting.
- Memory ownership.
- Error handling.
- Build configuration.
- ABI compatibility.
- Thread and GIL management.

Start with Python, then optimize with:

```
better algorithm
built-ins
NumPy
Numba
Cython
```

Use a C extension only when the performance requirement justifies the maintenance cost.

# 18. Optimization order

Use this order:

```
1. Measure.
2. Improve the algorithm.
3. Use better data structures.
4. Remove repeated work.
5. Reduce unnecessary allocation/copying.
6. Batch I/O.
7. Add caching where valid.
8. Use concurrency for waiting.
9. Use processes for CPU work.
10. Use native acceleration only for proven hotspots.
```

Avoid beginning with:

```
micro-optimizing variable names
adding __slots__ everywhere
rewriting everything in C
using multiprocessing for tiny functions
```

# 19. End-to-end profiling example

Suppose you have a ticket classifier:

```
def classify_tickets(tickets):
    results = []

    for ticket in tickets:
        text = ticket["text"].lower()

        if "payment" in text:
            category = "billing"
        elif "password" in text:
            category = "account_access"
        else:
            category = "general"

        results.append({
            "id": ticket["id"],
            "category": category,
        })

    return results
```

Profile:

```
python -m cProfile -s cumulative classifier.py
```

Memory profile:

```
import tracemalloc


tracemalloc.start()

results = classify_tickets(tickets)

snapshot = tracemalloc.take_snapshot()

for stat in snapshot.statistics("lineno")[:10]:
    print(stat)
```

Potential improvements might include:

- Stream results rather than building a giant list.
- Use a generator.
- Batch database writes.
- Avoid copying large ticket objects.
- Cache repeated classifications if valid.
- Profile the actual model/API call rather than optimizing keyword checks.

The profiler tells you what to investigate; it does not automatically tell you which optimization is semantically safe.

# 20. Practice exercises

## Exercise 1: `cProfile`

Create a function with an intentionally slow nested loop. Profile it with:

```
python -m cProfile -s cumulative app.py
```

Identify the hottest function.

## Exercise 2: `tracemalloc`

Allocate a large list, take snapshots before and after, and identify the line responsible for the largest memory increase.

## Exercise 3: `__slots__`

Create 100,000 instances of two classes:

- One normal class.
- One class with `__slots__`.

Compare memory using `tracemalloc`.

## Exercise 4: weak references

Create a `WeakValueDictionary` cache and observe what happens after deleting the last strong reference.

## Exercise 5: thread versus process

Run a CPU-heavy function using:

- Sequential execution.
- `ThreadPoolExecutor`.
- `ProcessPoolExecutor`.

Compare execution times.

## Exercise 6: generator optimization

Rewrite a function that builds a large intermediate list so it uses a generator pipeline.

# 21. Final mental model

```
cProfile
    → Which functions consume time?

py-spy
    → What is a live process doing?

Scalene
    → Which lines consume CPU and memory?

tracemalloc
    → Where are Python memory allocations growing?

gc
    → How is cyclic garbage being collected?

__slots__
    → Can many fixed-shape objects use less memory?

weakref
    → Can a cache/reference avoid keeping objects alive?

GIL
    → Why do threads usually not parallelize CPU-bound Python bytecode?

Free-threaded Python
    → Optional newer builds can execute Python threads in parallel,
      but compatibility and synchronization still matter.
```

For your AI-engineering systems:

```
Slow model/API calls       → async I/O, batching, caching, timeouts
Slow Python preprocessing  → better algorithms, generators, processes
Large ticket streams       → generators and streaming
Many small domain objects  → measure __slots__
Growing caches             → bounded caches or weak references
Unknown production issue   → py-spy or Scalene
Memory growth              → tracemalloc snapshots
CPU-heavy evaluation      → ProcessPoolExecutor, NumPy, Numba, or Cython
```

The main rule is:

> Never optimize the code you merely suspect is slow. Profile the real workload, identify the bottleneck, make one targeted change, and measure again.

Python’s standard tools support this workflow: `cProfile` for deterministic execution profiles, `tracemalloc` for allocation tracing, `gc` for garbage-collection diagnostics, and free-threaded builds as an evolving option for parallel threads.[[docs.python](https://docs.python.org/3/library/tracemalloc.html)][[docs.python](https://docs.python.org/3/library/gc.html)][[docs.python](https://docs.python.org/3/library/profile.html)][[docs.python](https://docs.python.org/3/howto/free-threading-python.html)]
