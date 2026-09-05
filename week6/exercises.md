# Performance, Internals & Optimization — Exercises

## Instructions

Solve each question independently. Measure before changing code. The questions describe outcomes but do not prescribe the optimization technique unless a tool is explicitly named.

Always compare correctness before and after an optimization.

---

## Exercise 1 — Establish a baseline

Measure the execution time of a function that processes 100,000 ticket titles.

Record the elapsed time and the number of output records.

---

## Exercise 2 — `timeit` comparison

Compare the execution time of:

```python
[x * 2 for x in values]
```

and an equivalent loop that appends values to a list.

Use multiple repetitions and report the results.

---

## Exercise 3 — `cProfile`

Create a program containing three functions:

```text
load_data
transform_data
save_data
```

Make one function intentionally slower than the others.

Profile the program and identify which function has the largest cumulative time.

---

## Exercise 4 — `pstats`

Save a profile to a file and use `pstats` to:

- Sort by cumulative time.
- Display the ten most expensive functions.
- Display callers of the slowest function.

---

## Exercise 5 — Memory snapshot

Use `tracemalloc` to compare memory before and after creating a large list of strings.

Display the ten lines responsible for the largest allocation differences.

---

## Exercise 6 — Peak memory

Measure current and peak traced memory while creating and consuming a large collection.

Compare the peak memory with a lazy processing version.

---

## Exercise 7 — Reference behavior

Create two variables that refer to the same mutable list.

Demonstrate that modifying one variable changes the object seen through the other variable.

Then create an independent shallow copy and demonstrate the difference.

---

## Exercise 8 — Cyclic references

Create two objects that refer to each other.

Delete the external references and use the garbage-collection interface to observe collection behavior.

---

## Exercise 9 — `gc` inspection

Inspect:

```text
gc.isenabled()
gc.get_count()
gc.get_threshold()
```

Manually trigger collection and record the returned count.

---

## Exercise 10 — Compare instance memory

Create two classes representing a point:

- A normal dynamic class.
- A fixed-attribute class.

Create many instances and compare memory usage with `tracemalloc`.

Verify that the fixed-attribute version rejects an undeclared attribute.

---

## Exercise 11 — Weak references

Create an object and a weak reference to it.

Show that the weak reference returns the object while a strong reference exists and returns `None` after the last strong reference is deleted.

---

## Exercise 12 — Weak-value cache

Create a weak-value cache for model objects.

Verify that the cache entry disappears after the model has no remaining strong references.

---

## Exercise 13 — Algorithmic improvement

Given a large list of allowed categories, compare membership testing with:

```text
a list
an appropriate alternative container
```

Measure the difference and verify that both produce the same logical results.

---

## Exercise 14 — Avoid intermediate collections

Create two functions that calculate the sum of squares from `0` to one million:

- One creates an intermediate collection.
- One processes values without retaining the whole collection.

Compare peak memory usage and verify equal results.

---

## Exercise 15 — Caching

Create a deterministic expensive function with repeated inputs.

Compare execution with and without caching.

Expose cache statistics and clear the cache.

---

## Exercise 16 — Threading and the GIL experiment

Run a CPU-heavy function:

```text
sequentially
with several threads
with several processes
```

Measure each version and explain the observed result.

---

## Exercise 17 — Free-threading investigation

Inspect the current interpreter configuration and determine whether it supports a free-threaded build.

Write the result in a readable form.

---

## Exercise 18 — Optimize only after profiling

Create a deliberately inefficient ticket transformation function.

Profile it, identify the dominant operation, improve it, and profile the revised version.

Report:

```text
old time
new time
speedup
```

---

## Exercise 19 — Native acceleration experiment

Implement a numerical function in ordinary Python and compare it with a suitable vectorized or compiled approach available in your environment.

Verify that both approaches produce equivalent results.

---

## Exercise 20 — Final optimization report

Choose one real data-processing function and produce a short report containing:

- The original implementation.
- The measured baseline.
- The identified bottleneck.
- One improvement.
- Correctness verification.
- New measurements.
- Memory observations.
- A reason why the improvement is worth its complexity.

# Practice rules

- Never claim an optimization without measuring.
- Keep the input size consistent when comparing versions.
- Separate CPU time, wall-clock time, and memory usage.
- Preserve behavior while optimizing.
- Prefer algorithmic improvements over micro-optimizations.
