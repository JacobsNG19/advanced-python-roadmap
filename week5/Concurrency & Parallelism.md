Concurrency means managing multiple tasks whose execution overlaps. Parallelism means multiple tasks physically executing at the same time. In Python, the right tool depends mainly on whether your work is **CPU-bound** or **I/O-bound**:

```
CPU-bound Python work → multiprocessing or process pools
I/O-bound work        → asyncio or threads
Mixed work            → combine tools carefully
```

Threads share memory inside one process; processes use separate memory and can bypass the GIL; `asyncio` uses cooperative scheduling in one thread; `concurrent.futures` gives a high-level interface over thread and process pools.[[docs.python](https://docs.python.org/3/library/multiprocessing.html)][[docs.python](https://docs.python.org/3/library/threading.html)][[docs.python](https://docs.python.org/3/library/concurrent.futures.html)]

# 1. Concurrency versus parallelism

## Concurrency

Several tasks make progress over the same period.

```
Task A starts
Task A waits for network
Task B runs
Task B waits
Task A resumes
```

This is common with:

- HTTP requests.
- Database queries.
- File operations.
- Timers.
- Socket communication.

## Parallelism

Several tasks execute simultaneously on different CPU cores.

```
Core 1 → task A
Core 2 → task B
Core 3 → task C
```

This is useful for:

- Image processing.
- Numerical computation.
- Large data transformations.
- CPU-heavy model preprocessing.
- Compression.
- Simulation.
- Cryptographic or mathematical work.

## Important distinction

Concurrency can improve total time even without parallel CPU execution:

```
One task waits → another task uses the waiting time
```

# 2. CPU-bound versus I/O-bound

## I/O-bound work

The program spends much of its time waiting for external systems.

```
response = await http_request()
```

Examples:

- Calling an LLM API.
- Reading a database.
- Waiting for a file.
- Downloading data.
- Waiting for a subprocess.
- Receiving a WebSocket message.

Best candidates:

```
asyncio
threads
```

## CPU-bound work

The program spends much of its time computing.

```
for number in range(100_000_000):
    result += number * number
```

Examples:

- Parsing huge data with pure Python.
- Image transformations.
- Compression.
- Feature engineering.
- Large simulations.
- CPU-heavy token processing.

Best candidates:

```
multiprocessing
ProcessPoolExecutor
native/vectorized libraries
```

# 3. The GIL

The Global Interpreter Lock, or GIL, historically means that only one thread executes Python bytecode at a time within a standard CPython process.

Therefore, threads often do not speed up CPU-heavy pure-Python code.

```
# CPU-bound Python work
def calculate():
    total = 0

    for number in range(20_000_000):
        total += number * number

    return total
```

Running this with many ordinary threads may not produce the parallel speedup you expect.

The GIL does not prevent threads from being useful. Threads can overlap I/O because a thread can wait while another thread runs. Python’s threading documentation explains that the GIL limits performance gains for CPU-bound threaded code, while threads remain useful for many concurrency scenarios. It also notes that free-threaded builds can disable the GIL, but those builds are not the default.[[docs.python](https://docs.python.org/3/library/threading.html)]

## Practical rule

```
CPU-bound pure Python → processes
I/O-bound waiting      → threads or asyncio
```

Some native libraries release the GIL during heavy computation, so threads can sometimes help with operations implemented in optimized C, C++, or Rust.

# 4. Threading basics

The `threading` module runs multiple threads inside one process.

```
import threading
import time


def worker(name):
    print(f"{name} started.")
    time.sleep(2)
    print(f"{name} finished.")
```

Create threads:

```
thread_a = threading.Thread(
    target=worker,
    args=("A",),
)

thread_b = threading.Thread(
    target=worker,
    args=("B",),
)
```

Start and wait:

```
thread_a.start()
thread_b.start()

thread_a.join()
thread_b.join()
```

Output:

```
A started.
B started.
A finished.
B finished.
```

Approximate duration:

```
2 seconds
```

instead of:

```
4 seconds
```

The threads overlap while waiting.

## `start()` versus `run()`

Use:

```
thread.start()
```

This creates a new thread.

Do not use:

```
thread.run()
```

if you want concurrency. Calling `run()` directly executes in the current thread.

## `join()`

```
thread.join()
```

means:

```
Wait for this thread to finish.
```

With a timeout:

```
thread.join(timeout=3)
```

Then check:

```
if thread.is_alive():
    print("Thread is still running.")
```

# 5. Thread return values and exceptions

A thread target’s return value is not automatically returned by `join()`.

Bad expectation:

```
result = thread.join()
```

`join()` returns `None`.

Use a shared result container:

```
import threading


def worker(result):
    result.append(10 * 2)


results = []

thread = threading.Thread(
    target=worker,
    args=(results,),
)

thread.start()
thread.join()

print(results)
```

For most task-style work, `ThreadPoolExecutor` is cleaner because it returns `Future` objects.

# 6. Thread safety and race conditions

A race condition occurs when multiple threads access shared mutable state and the final result depends on timing.

```
import threading


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
```

This may look simple, but in concurrent code, multiple threads can interfere with the read-modify-write sequence.

Use a lock:

```
import threading


class SafeCounter:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.value += 1
```

```
counter = SafeCounter()

threads = [
    threading.Thread(
        target=lambda: [
            counter.increment()
            for _ in range(10_000)
        ]
    )
    for _ in range(4)
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(counter.value)
```

Expected:

```
40000
```

A lock makes the critical section exclusive.

Python lock objects can be used as context managers:

```
with lock:
    shared_state.update(...)
```

The threading documentation recommends this pattern because acquisition happens on entry and release happens on exit, including when exceptions occur.[[docs.python](https://docs.python.org/3/library/threading.html)]

# 7. Locks

## `Lock`

Use for basic mutual exclusion:

```
lock = threading.Lock()

with lock:
    # Only one thread at a time enters here.
    shared_data.append(item)
```

## `RLock`

An `RLock` can be acquired multiple times by the same thread.

```
lock = threading.RLock()
```

Use it when a method holding the lock calls another method that also acquires the same lock.

```
class Resource:
    def __init__(self):
        self._lock = threading.RLock()

    def outer(self):
        with self._lock:
            return self.inner()

    def inner(self):
        with self._lock:
            return "Done"
```

A normal `Lock` could deadlock in this recursive acquisition pattern.

## Semaphore

A semaphore limits how many threads can enter a region simultaneously.

```
semaphore = threading.Semaphore(3)
```

```
def call_api(url):
    with semaphore:
        return make_request(url)
```

This is useful for:

- API rate limits.
- Database connection limits.
- File descriptors.
- External services.

# 8. Threading queues

Use `queue.Queue` for safe producer-consumer communication.

```
import queue
import threading
import time
```

Producer:

```
def producer(items, work_queue):
    for item in items:
        work_queue.put(item)

    work_queue.put(None)
```

Consumer:

```
def consumer(work_queue):
    while True:
        item = work_queue.get()

        try:
            if item is None:
                return

            print(f"Processing {item}")
            time.sleep(0.2)

        finally:
            work_queue.task_done()
```

Run:

```
work_queue = queue.Queue()

producer_thread = threading.Thread(
    target=producer,
    args=(
        ["T-001", "T-002", "T-003"],
        work_queue,
    ),
)

consumer_thread = threading.Thread(
    target=consumer,
    args=(work_queue,),
)

producer_thread.start()
consumer_thread.start()

work_queue.join()
consumer_thread.join()
```

`queue.Queue` handles thread-safe communication without requiring you to manually protect every operation.

Use queues for:

```
producer → worker threads → consumer
```

Examples:

- Reading tickets and classifying them.
- Downloading files and processing them.
- Receiving events and writing them.
- Background logging.
- Task workers.

# 9. `ThreadPoolExecutor`

`concurrent.futures` provides a high-level interface for asynchronously executing callables using threads or processes.[[docs.python](https://docs.python.org/3/library/concurrent.futures.html)]

```
from concurrent.futures import ThreadPoolExecutor
import time


def fetch(item):
    time.sleep(1)
    return f"Fetched {item}"
```

Use a thread pool:

```
with ThreadPoolExecutor(
    max_workers=3
) as executor:
    results = list(
        executor.map(
            fetch,
            ["A", "B", "C"],
        )
    )

print(results)
```

Output:

```
['Fetched A', 'Fetched B', 'Fetched C']
```

This is cleaner than manually creating and joining threads.

# 10. Futures

`submit()` schedules work and returns a `Future`.

```
from concurrent.futures import ThreadPoolExecutor


def add(first, second):
    return first + second


with ThreadPoolExecutor(
    max_workers=2
) as executor:
    future = executor.submit(add, 2, 3)

    print(future.done())

    result = future.result()

    print(result)
```

Output:

```
False
5
```

Calling:

```
future.result()
```

waits until the task finishes and returns its result.

If the worker raises an exception, `future.result()` raises that exception in the calling thread.

# 11. `as_completed`

`executor.map()` returns results in input order.

Use `as_completed()` when you want results as soon as each task finishes.

```
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
import time


def fetch(name, delay):
    time.sleep(delay)
    return name
```

```
jobs = {
    "A": 2,
    "B": 1,
    "C": 3,
}

with ThreadPoolExecutor(
    max_workers=3
) as executor:
    futures = {
        executor.submit(fetch, name, delay): name
        for name, delay in jobs.items()
    }

    for future in as_completed(futures):
        name = futures[future]

        try:
            result = future.result()
            print(f"{name}: {result}")

        except Exception as error:
            print(f"{name} failed: {error}")
```

Likely completion order:

```
B
A
C
```

Use this for:

- Progress reporting.
- Fastest-result selection.
- Handling independent requests.
- Streaming completed work to a consumer.

# 12. Thread pool caveats

Avoid deadlocks where a worker waits for another future from the same small pool.

```
from concurrent.futures import ThreadPoolExecutor


def outer(executor):
    future = executor.submit(inner)
    return future.result()


def inner():
    return "done"
```

With only one worker:

```
with ThreadPoolExecutor(
    max_workers=1
) as executor:
    executor.submit(
        outer,
        executor,
    ).result()
```

The worker running `outer()` waits for `inner()`, but no free worker exists to run `inner()`.

Design tasks so workers do not synchronously wait for work submitted to the same exhausted pool.

# 13. Multiprocessing

`multiprocessing` uses separate processes rather than threads.

Each process has:

- Its own Python interpreter.
- Its own memory space.
- Its own GIL.
- Independent execution.

This allows CPU-bound Python code to use multiple CPU cores. The multiprocessing documentation describes it as a way to side-step the GIL using subprocesses and leverage multiple processors.[[docs.python](https://docs.python.org/3/library/multiprocessing.html)]

## Basic process

```
from multiprocessing import Process


def worker(name):
    print(f"Worker {name} running.")


if __name__ == "__main__":
    process = Process(
        target=worker,
        args=("A",),
    )

    process.start()
    process.join()
```

Always protect process-starting code with:

```
if __name__ == "__main__":
```

This is especially important on systems that use spawn-based process creation.

# 14. Process communication

Processes do not normally share ordinary Python variables.

Use:

- Queues.
- Pipes.
- Shared values.
- Shared arrays.
- Managers.
- Files/databases.
- Message brokers.

## Process queue

```
from multiprocessing import Process, Queue


def worker(queue):
    queue.put("Finished processing.")


if __name__ == "__main__":
    queue = Queue()

    process = Process(
        target=worker,
        args=(queue,),
    )

    process.start()

    print(queue.get())

    process.join()
```

## Why process communication costs more

Data crossing a process boundary usually must be serialized and transferred.

This makes processes more expensive than threads for tiny tasks.

Use process pools for sufficiently large CPU tasks, not every small calculation.

# 15. `ProcessPoolExecutor`

For most application-level process parallelism, use:

```
from concurrent.futures import ProcessPoolExecutor


def square(number):
    return number * number
```

```
if __name__ == "__main__":
    with ProcessPoolExecutor(
        max_workers=4
    ) as executor:
        results = list(
            executor.map(
                square,
                range(10),
            )
        )

    print(results)
```

`ProcessPoolExecutor` uses processes and can bypass the GIL, but submitted functions and results must be pickleable, and the `__main__` module must be importable by worker processes.[[docs.python](https://docs.python.org/3/library/concurrent.futures.html)]

## Process-pool restrictions

This may fail:

```
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(
                lambda x: x * x,
                range(10),
            )
        )
```

Lambdas are not generally pickleable.

Use a module-level function:

```
def square(number):
    return number * number
```

Also avoid passing:

- Open files.
- Locks that cannot be serialized.
- Live sockets.
- Database connections.
- Async event-loop objects.
- Objects tied to a specific process.

# 16. Threads versus processes

|Feature|Threads|Processes|
|---|---|---|
|Memory|Shared|Separate|
|Startup|Usually cheaper|More expensive|
|Communication|Easy but must synchronize|Requires serialization/IPC|
|CPU-bound pure Python|Usually limited by GIL|Good parallelism|
|I/O-bound work|Good|Usually unnecessary|
|Shared state risk|Race conditions|Less shared-state risk|
|Failure isolation|Lower|Higher|
|Best use|I/O and blocking libraries|CPU-heavy computation|

# 17. `asyncio` fundamentals

`asyncio` provides cooperative concurrency using:

```
async
await
```

It is usually single-threaded and relies on tasks voluntarily yielding at await points.

```
import asyncio


async def fetch(name, delay):
    print(f"{name} started.")
    await asyncio.sleep(delay)
    print(f"{name} finished.")
    return name
```

Run:

```
asyncio.run(fetch("A", 1))
```

## The event loop

The event loop:

1. Runs a coroutine.
2. Reaches an await point.
3. Suspends that coroutine.
4. Runs another ready task.
5. Resumes the original task when its awaited operation is ready.

```
task A → awaits network
task B → runs
task B → awaits database
task A → network response arrives
task A → resumes
```

The normal entry point is:

```
asyncio.run(main())
```

which manages the event loop lifecycle for the top-level async program.[[docs.python](https://docs.python.org/3/library/asyncio-runner.html)]

# 18. Sequential async code

```
async def main():
    first = await fetch("A", 2)
    second = await fetch("B", 2)

    print(first, second)
```

This is asynchronous but sequential.

Approximate duration:

```
4 seconds
```

# 19. Concurrent tasks

```
async def main():
    task_a = asyncio.create_task(
        fetch("A", 2)
    )

    task_b = asyncio.create_task(
        fetch("B", 2)
    )

    result_a = await task_a
    result_b = await task_b

    print(result_a, result_b)
```

The tasks overlap while waiting.

`create_task()` schedules a coroutine to run concurrently and returns a task object.[[docs.python](https://docs.python.org/3/library/asyncio-task.html)]

# 20. `asyncio.gather`

```
async def main():
    results = await asyncio.gather(
        fetch("A", 2),
        fetch("B", 1),
        fetch("C", 3),
    )

    print(results)
```

Approximate duration:

```
3 seconds
```

Results preserve input order:

```
["A", "B", "C"]
```

Even if B completes first.

## Exceptions

Default:

```
await asyncio.gather(
    operation_a(),
    operation_b(),
)
```

If one operation raises, the exception propagates.

Collect exceptions:

```
results = await asyncio.gather(
    operation_a(),
    operation_b(),
    return_exceptions=True,
)
```

Then inspect each result.

# 21. Structured concurrency with `TaskGroup`

```
async def main():
    async with asyncio.TaskGroup() as group:
        task_a = group.create_task(
            fetch("A", 2)
        )

        task_b = group.create_task(
            fetch("B", 1)
        )

    print(task_a.result())
    print(task_b.result())
```

Task groups manage related tasks as one structured unit. If one task fails, related tasks are generally cancelled and the group waits for them to finish cancellation. Python’s asyncio documentation presents `TaskGroup` as an alternative to `gather()` that provides stronger safety through structured concurrency.[[docs.python](https://docs.python.org/3/library/asyncio-task.html)]

Use:

```
gather → simple concurrent result collection
TaskGroup → related tasks with coordinated lifecycle and failure handling
```

# 22. Async timeouts

```
async def slow_operation():
    await asyncio.sleep(10)
```

```
async def main():
    try:
        async with asyncio.timeout(3):
            await slow_operation()

    except TimeoutError:
        print("Operation timed out.")
```

Use a timeout around every external operation that could wait indefinitely.

For one awaitable:

```
await asyncio.wait_for(
    slow_operation(),
    timeout=3,
)
```

For a block containing several operations:

```
async with asyncio.timeout(3):
    await operation_a()
    await operation_b()
```

# 23. Cancellation

```
async def worker():
    try:
        while True:
            await asyncio.sleep(1)
            print("Working.")

    except asyncio.CancelledError:
        print("Cleaning up.")
        raise
```

```
async def main():
    task = asyncio.create_task(worker())

    await asyncio.sleep(2)

    task.cancel()

    try:
        await task

    except asyncio.CancelledError:
        print("Task stopped.")
```

Always clean up cancellation and usually re-raise `CancelledError`.

Cancellation is used by:

- Timeouts.
- Task groups.
- Application shutdown.
- Request cancellation.
- Supervisor systems.

# 24. Async generators

An async generator uses:

```
async def
yield
```

```
async def event_stream():
    for event in [
        "ticket.created",
        "ticket.classified",
        "ticket.closed",
    ]:
        await asyncio.sleep(0.5)
        yield event
```

Consume it:

```
async def main():
    async for event in event_stream():
        print(event)
```

Use async generators for:

- Streaming model output.
- WebSocket messages.
- Async database cursors.
- Event streams.
- Batched API results.

# 25. `aiohttp`

`aiohttp` is an asynchronous HTTP client/server framework for `asyncio`. It is not part of Python’s standard library.

Install:

```
python -m pip install aiohttp
```

Basic client:

```
import asyncio
import aiohttp


async def fetch_text(
    session: aiohttp.ClientSession,
    url: str,
) -> str:
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()
```

Use one session for multiple requests:

```
async def main():
    urls = [
        "https://example.com",
        "https://example.org",
    ]

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[
                fetch_text(session, url)
                for url in urls
            ]
        )

    for result in results:
        print(result[:100])
```

The aiohttp client documentation uses `ClientSession`, `async with session.get(...)`, and `await response.text()` for asynchronous HTTP requests.[[docs.aiohttp](https://docs.aiohttp.org/en/stable/client_quickstart.html)][[docs.aiohttp](http://docs.aiohttp.org/en/stable/index.html)]

## Add a timeout

```
timeout = aiohttp.ClientTimeout(
    total=10
)
```

```
async with aiohttp.ClientSession(
    timeout=timeout
) as session:
    ...
```

## Limit concurrency

```
semaphore = asyncio.Semaphore(10)
```

```
async def limited_fetch(session, url):
    async with semaphore:
        return await fetch_text(session, url)
```

Do not launch thousands of requests without a concurrency limit.

# 26. Async blocking mistakes

This blocks the event loop:

```
import time


async def bad():
    time.sleep(5)
```

Use:

```
await asyncio.sleep(5)
```

For a blocking synchronous function:

```
async def main():
    result = await asyncio.to_thread(
        blocking_function
    )
```

For CPU-heavy work, use a process pool rather than occupying the event loop.

# 27. Choosing the right tool

|Workload|Recommended tool|
|---|---|
|Many HTTP requests with async libraries|`asyncio`|
|Blocking synchronous HTTP SDK|`ThreadPoolExecutor`|
|Blocking file or database API|Threads or `asyncio.to_thread`|
|CPU-heavy pure Python|`ProcessPoolExecutor`|
|Large numerical work in native libraries|Benchmark threads/processes|
|Independent CPU jobs|Multiprocessing|
|Shared-memory I/O workers|Threads + `queue.Queue`|
|Async producer/consumer|`asyncio.Queue`|
|Need simple pool interface|`concurrent.futures`|

## Decision process

Ask:

1. Is the task mostly waiting?
2. Is the library asynchronous?
3. Is the task CPU-heavy?
4. Does the work need shared mutable state?
5. Is the function serializable for a process pool?
6. Do I need cancellation and deadlines?
7. How many concurrent operations can the dependency handle?

# 28. Mixed architecture

A common AI pipeline:

```
async HTTP requests
        ↓
CPU-heavy preprocessing
        ↓
async model API calls
        ↓
CPU-heavy evaluation
        ↓
database writes
```

Possible design:

```
asyncio → HTTP and database I/O
process pool → CPU-heavy transformation/evaluation
asyncio → external model calls
```

Example:

```
import asyncio
from concurrent.futures import ProcessPoolExecutor


def cpu_heavy_score(data):
    return sum(
        value * value
        for value in data
    )


async def fetch_data():
    await asyncio.sleep(1)
    return list(range(100_000))


async def main():
    data = await fetch_data()

    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as pool:
        score = await loop.run_in_executor(
            pool,
            cpu_heavy_score,
            data,
        )

    print(score)
```

For a simple one-off blocking function, use:

```
await asyncio.to_thread(...)
```

For CPU-bound work, use a process pool.

# 29. Threading versus asyncio

Both can handle I/O, but they differ.

|Feature|Threads|Asyncio|
|---|---|---|
|Programming style|Blocking functions|`async`/`await`|
|Works with sync libraries|Naturally|Requires `to_thread`|
|Scales to many connections|Can, but threads cost more|Often excellent|
|Cancellation|More limited|Built into task model|
|Shared state|Direct shared memory|Usually one-thread cooperative state|
|Debugging|Thread races/deadlocks|Await/task lifecycle issues|
|Best when|Existing blocking APIs|Async-native APIs and many concurrent operations|

Use threads when:

```
You already have reliable synchronous libraries.
```

Use asyncio when:

```
You have async-native libraries and many concurrent I/O operations.
```

# 30. Thread safety principles

Prefer:

```
immutable data
message passing
queues
small critical sections
```

Avoid large shared mutable structures.

Good:

```
with lock:
    shared_counter += 1
```

Better architecture:

```
worker computes result
worker puts result on queue
one consumer owns shared state
```

This reduces race conditions.

Thread safety does not mean your code is automatically safe because of the GIL. The GIL does not make compound application-level operations logically atomic.

# 31. Process safety principles

For process pools:

- Put worker functions at module level.
- Protect entry points with `if __name__ == "__main__":`.
- Pass serializable arguments.
- Avoid passing live resources.
- Keep tasks sufficiently large to justify process overhead.
- Be careful with memory duplication.
- Handle worker exceptions through futures.

# 32. Practice exercises

## Exercise 1: Thread pool

Use `ThreadPoolExecutor` to simulate fetching five URLs with `time.sleep()`.

Print results as they complete with `as_completed()`.

## Exercise 2: Process pool

Use `ProcessPoolExecutor` to calculate squares of large numbers.

## Exercise 3: Thread-safe counter

Create a counter updated by four threads. Protect it with `threading.Lock`.

## Exercise 4: Async gather

Create three async operations with different delays and run them with `asyncio.gather()`.

## Exercise 5: Async timeout

Create an operation that sleeps for five seconds and cancel it after two seconds.

## Exercise 6: aiohttp client

Use one `ClientSession` to fetch several URLs concurrently with a semaphore.

## Exercise 7: Mixed pipeline

Fetch data asynchronously, send CPU-heavy processing to a process pool, then print results asynchronously.

# 33. Exercise answers

## Exercise 1 answer

```
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
import time


def fetch(name, delay):
    time.sleep(delay)
    return f"{name} complete"


jobs = {
    "A": 2,
    "B": 1,
    "C": 3,
}

with ThreadPoolExecutor(
    max_workers=3
) as executor:
    futures = {
        executor.submit(
            fetch,
            name,
            delay,
        ): name
        for name, delay in jobs.items()
    }

    for future in as_completed(futures):
        print(future.result())
```

## Exercise 2 answer

```
from concurrent.futures import ProcessPoolExecutor


def square(number):
    return number * number


if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(
                square,
                range(10),
            )
        )

    print(results)
```

## Exercise 3 answer

```
import threading


class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
```

```
counter = Counter()


def work():
    for _ in range(10_000):
        counter.increment()


threads = [
    threading.Thread(target=work)
    for _ in range(4)
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(counter.value)
```

## Exercise 4 answer

```
import asyncio


async def operation(name, delay):
    await asyncio.sleep(delay)
    return f"{name} complete"


async def main():
    results = await asyncio.gather(
        operation("A", 2),
        operation("B", 1),
        operation("C", 3),
    )

    print(results)


asyncio.run(main())
```

## Exercise 5 answer

```
import asyncio


async def slow_operation():
    await asyncio.sleep(5)


async def main():
    try:
        async with asyncio.timeout(2):
            await slow_operation()

    except TimeoutError:
        print("Timed out.")


asyncio.run(main())
```

## Exercise 6 answer

```
import asyncio
import aiohttp


async def fetch(
    session,
    semaphore,
    url,
):
    async with semaphore:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
```

```
async def main():
    urls = [
        "https://example.com",
        "https://example.org",
        "https://www.python.org",
    ]

    semaphore = asyncio.Semaphore(2)
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:
        results = await asyncio.gather(
            *[
                fetch(
                    session,
                    semaphore,
                    url,
                )
                for url in urls
            ]
        )

    for result in results:
        print(result[:80])


asyncio.run(main())
```

## Exercise 7 answer

```
import asyncio
from concurrent.futures import ProcessPoolExecutor


def calculate_score(values):
    return sum(
        value * value
        for value in values
    )


async def fetch_values():
    await asyncio.sleep(1)
    return list(range(100_000))


async def main():
    values = await fetch_values()
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as pool:
        score = await loop.run_in_executor(
            pool,
            calculate_score,
            values,
        )

    print(score)


asyncio.run(main())
```

# 34. Final mental model

```
Threading
  → shared-memory concurrency
  → useful for blocking I/O
  → protect shared state with locks
  → GIL limits CPU-bound pure Python

Multiprocessing
  → separate-memory parallelism
  → useful for CPU-bound work
  → communication is more expensive
  → arguments/results must be serializable

concurrent.futures
  → high-level executor interface
  → ThreadPoolExecutor for threads
  → ProcessPoolExecutor for processes
  → Future objects represent results

asyncio
  → cooperative concurrency
  → one event loop schedules tasks
  → async/await for non-blocking I/O
  → gather for simple concurrent collection
  → TaskGroup for structured concurrency
  → async generators for streams
  → aiohttp for async HTTP
```

The practical choice is:

```
# Many async HTTP/database operations
asyncio

# Existing synchronous blocking APIs
ThreadPoolExecutor

# CPU-heavy pure Python
ProcessPoolExecutor

# Small shared-memory I/O workers
threading + queue.Queue
```

For your AI-engineering systems, a typical architecture is:

```
asyncio + aiohttp
    → concurrent model/API requests

Semaphore
    → provider concurrency limits

TaskGroup
    → structured task lifecycle

ProcessPoolExecutor
    → CPU-heavy parsing/evaluation

Databases and queues
    → durable coordination between stages
```

Start with `concurrent.futures` for simple pools, `asyncio` for async-native I/O, and process pools for CPU-heavy work. Do not choose concurrency tools based on fashion; choose based on the workload, library support, cancellation requirements, and data-sharing model.[[docs.python](https://docs.python.org/3/library/multiprocessing.html)][[docs.python](https://docs.python.org/3/library/threading.html)][[docs.python](https://docs.python.org/3/library/concurrent.futures.html)][[docs.aiohttp](https://docs.aiohttp.org/en/stable/client_quickstart.html)]
