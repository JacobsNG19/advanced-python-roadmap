# Concurrency & Parallelism — Exercises

## Instructions

Solve each question independently. Choose your own implementation. The requirements describe behavior without prescribing which concurrency mechanism must be used, except where a specific API is explicitly part of the question.

Use small delays and small workloads while experimenting.

---

## Exercise 1 — Overlapping waiting operations

Create a program with two operations that each wait for two seconds.

Run them so the total elapsed time is close to two seconds rather than four seconds.

---

## Exercise 2 — Thread workers

Create three worker executions named `A`, `B`, and `C`.

Each worker should wait for one second and report when it starts and finishes.

Wait until all workers have completed before the program exits.

---

## Exercise 3 — Thread-safe counter

Create a counter updated by four concurrent workers.

Each worker must increment the counter 10,000 times.

The final value must be exactly 40,000.

---

## Exercise 4 — Producer and consumer

Create a producer that places five values into a shared work queue and a consumer that processes every value.

The consumer must signal completion for every item.

---

## Exercise 5 — Thread pool

Use a pool of workers to process five simulated I/O tasks.

Each task should return its task name after a short delay.

Collect all results.

---

## Exercise 6 — Results as completed

Create tasks with different delays and display each result immediately when its task finishes rather than waiting for input-order results.

---

## Exercise 7 — Thread exception handling

Create a worker that raises an exception.

Ensure the caller receives and handles that exception after waiting for the work to finish.

---

## Exercise 8 — CPU workload comparison

Create a CPU-heavy calculation and compare:

```text
sequential execution
thread-pool execution
process-pool execution
```

Record the elapsed time for each approach.

---

## Exercise 9 — Separate process

Create a separate process that computes a value and sends the result back to the parent process.

The parent must wait for the child process and display the result.

---

## Exercise 10 — Process pool

Use a process pool to calculate the square of a sequence of integers.

The solution must work when the file is executed as a script on systems that use spawned processes.

---

## Exercise 11 — Async coroutine

Create an asynchronous operation that waits for one second and returns a result.

Run it from an asynchronous entry point.

---

## Exercise 12 — Async concurrent tasks

Create three asynchronous operations with delays of two, one, and three seconds.

Run them concurrently and preserve the result order based on the order in which they were submitted.

---

## Exercise 13 — Async task failure

Create two asynchronous operations where one succeeds and one raises an exception.

Handle the exception without crashing the entire demonstration program.

---

## Exercise 14 — Async timeout

Create an operation that waits for five seconds.

Stop waiting after two seconds and handle the timeout cleanly.

---

## Exercise 15 — Task cancellation

Create a repeating asynchronous worker.

Start it, allow it to work briefly, cancel it, and ensure cleanup happens before the cancellation completes.

---

## Exercise 16 — Structured concurrency

Create two related asynchronous operations inside a task group.

Verify that the parent waits for both tasks.

Also observe what happens when one related task fails.

---

## Exercise 17 — Async generator

Create an asynchronous event source that produces three events with a short delay.

Consume the events in order.

---

## Exercise 18 — Async HTTP client

Use an asynchronous HTTP client to request several public URLs concurrently.

Requirements:

- Reuse one client session.
- Apply a total timeout.
- Limit simultaneous requests.
- Handle request failures.

---

## Exercise 19 — Mixed async and CPU work

Create an asynchronous function that obtains data after a delay, then sends CPU-heavy processing to a process pool without blocking the event loop.

---

## Exercise 20 — Choose the appropriate tool

For each workload, state whether you would choose threads, processes, asyncio, or a combination:

1. Calling 100 HTTP APIs using an async HTTP client.
2. Running a CPU-heavy pure-Python transformation.
3. Calling a blocking third-party SDK from an async application.
4. Processing messages from a shared in-memory queue.
5. Running independent model evaluations that consume several CPU cores.

Explain each choice.

---

## Exercise 21 — Final concurrent ticket pipeline

Build a pipeline with these stages:

```text
asynchronous ticket retrieval
        ↓
limited concurrent classification
        ↓
CPU-heavy score calculation
        ↓
structured result collection
```

The pipeline must:

- Apply a concurrency limit to external-style operations.
- Apply timeouts.
- Handle one failed classification without losing every successful result.
- Use a process pool for the CPU-heavy score calculation.

# Practice rules

- Measure elapsed time where appropriate.
- Test failure and cancellation paths.
- Do not use blocking functions directly inside asynchronous code.
- Do not create unlimited concurrent external requests.
- Protect process entry points with the correct main guard.
