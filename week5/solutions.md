# Concurrency & Parallelism — Solutions

These solutions correspond to:

```text
Concurrency & Parallelism - Exercises.md
```

---

## Exercise 1 — Overlapping waiting operations

```python
import asyncio


async def wait_operation(name):
    print(f"{name} started")
    await asyncio.sleep(2)
    print(f"{name} finished")
    return name


async def main():
    results = await asyncio.gather(
        wait_operation("A"),
        wait_operation("B"),
    )

    print(results)


asyncio.run(main())
```

The operations overlap while waiting, so the total duration is close to two seconds.

---

## Exercise 2 — Thread workers

```python
import threading
import time


def worker(name):
    print(f"{name} started")
    time.sleep(1)
    print(f"{name} finished")


threads = [
    threading.Thread(
        target=worker,
        args=(name,),
    )
    for name in ["A", "B", "C"]
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
```

`start()` begins a new thread. `join()` waits for completion.

---

## Exercise 3 — Thread-safe counter

```python
import threading


class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1


counter = Counter()


def worker():
    for _ in range(10_000):
        counter.increment()


threads = [
    threading.Thread(target=worker)
    for _ in range(4)
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

assert counter.value == 40_000
```

The lock protects the read-modify-write operation.

---

## Exercise 4 — Producer and consumer

```python
import queue
import threading


def producer(work_queue):
    for value in range(5):
        work_queue.put(value)

    work_queue.put(None)


def consumer(work_queue, results):
    while True:
        value = work_queue.get()

        try:
            if value is None:
                return

            results.append(value * 2)
        finally:
            work_queue.task_done()


work_queue = queue.Queue()
results = []

producer_thread = threading.Thread(
    target=producer,
    args=(work_queue,),
)

consumer_thread = threading.Thread(
    target=consumer,
    args=(work_queue, results),
)

producer_thread.start()
consumer_thread.start()

work_queue.join()
producer_thread.join()
consumer_thread.join()

assert sorted(results) == [0, 2, 4, 6, 8]
```

The sentinel `None` tells the consumer to stop. `task_done()` must be called for every item retrieved from the queue.

---

## Exercise 5 — Thread pool

```python
from concurrent.futures import ThreadPoolExecutor
import time


def process_task(name):
    time.sleep(0.2)
    return f"{name} complete"


with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(
        executor.map(
            process_task,
            ["A", "B", "C", "D", "E"],
        )
    )

assert len(results) == 5
```

A thread pool is convenient for blocking I/O-style tasks.

---

## Exercise 6 — Results as completed

```python
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
import time


def process_task(name, delay):
    time.sleep(delay)
    return name


jobs = {
    "A": 0.3,
    "B": 0.1,
    "C": 0.2,
}

completed = []

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(
            process_task,
            name,
            delay,
        ): name
        for name, delay in jobs.items()
    }

    for future in as_completed(futures):
        completed.append(future.result())

assert completed[0] == "B"
assert set(completed) == {"A", "B", "C"}
```

`as_completed()` yields futures in completion order.

---

## Exercise 7 — Thread exception handling

```python
from concurrent.futures import ThreadPoolExecutor


def failing_worker():
    raise ValueError("Worker failed.")


with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(failing_worker)

    try:
        future.result()
    except ValueError as error:
        assert str(error) == "Worker failed."
```

The exception is re-raised when the caller requests the future’s result.

---

## Exercise 8 — CPU workload comparison

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


def measure(function, values):
    start = perf_counter()
    results = [function(value) for value in values]
    elapsed = perf_counter() - start
    return results, elapsed


if __name__ == "__main__":
    limits = [500_000] * 4

    sequential_results, sequential_time = measure(
        cpu_work,
        limits,
    )

    with ThreadPoolExecutor(max_workers=4) as executor:
        start = perf_counter()
        thread_results = list(
            executor.map(cpu_work, limits)
        )
        thread_time = perf_counter() - start

    with ProcessPoolExecutor(max_workers=4) as executor:
        start = perf_counter()
        process_results = list(
            executor.map(cpu_work, limits)
        )
        process_time = perf_counter() - start

    assert sequential_results == thread_results
    assert sequential_results == process_results

    print(sequential_time)
    print(thread_time)
    print(process_time)
```

The exact timings depend on hardware and workload size. The point is to measure rather than assume.

---

## Exercise 9 — Separate process

```python
from multiprocessing import Process, Queue


def worker(queue):
    queue.put(21 * 2)


if __name__ == "__main__":
    queue = Queue()
    process = Process(
        target=worker,
        args=(queue,),
    )

    process.start()
    result = queue.get()
    process.join()

    assert result == 42
```

The queue transfers data between separate processes.

---

## Exercise 10 — Process pool

```python
from concurrent.futures import ProcessPoolExecutor


def square(number):
    return number * number


if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(square, range(10))
        )

    assert results == [
        number * number
        for number in range(10)
    ]
```

The main guard is required for reliable process spawning.

---

## Exercise 11 — Async coroutine

```python
import asyncio


async def operation():
    await asyncio.sleep(1)
    return "complete"


async def main():
    result = await operation()
    assert result == "complete"


asyncio.run(main())
```

---

## Exercise 12 — Async concurrent tasks

```python
import asyncio


async def operation(name, delay):
    await asyncio.sleep(delay)
    return name


async def main():
    results = await asyncio.gather(
        operation("A", 2),
        operation("B", 1),
        operation("C", 3),
    )

    assert results == ["A", "B", "C"]


asyncio.run(main())
```

`gather()` preserves input order even though completion order differs.

---

## Exercise 13 — Async task failure

```python
import asyncio


async def successful():
    await asyncio.sleep(0.01)
    return "success"


async def failing():
    await asyncio.sleep(0.01)
    raise ValueError("Failure")


async def main():
    results = await asyncio.gather(
        successful(),
        failing(),
        return_exceptions=True,
    )

    assert results[0] == "success"
    assert isinstance(results[1], ValueError)


asyncio.run(main())
```

`return_exceptions=True` makes exceptions appear in the results list.

---

## Exercise 14 — Async timeout

```python
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

The timeout is caught outside the timeout context.

---

## Exercise 15 — Task cancellation

```python
import asyncio


async def worker(events):
    try:
        while True:
            events.append("working")
            await asyncio.sleep(0.05)
    except asyncio.CancelledError:
        events.append("cleanup")
        raise


async def main():
    events = []
    task = asyncio.create_task(worker(events))

    await asyncio.sleep(0.12)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

    assert "working" in events
    assert events[-1] == "cleanup"


asyncio.run(main())
```

Cleanup runs before cancellation completes.

---

## Exercise 16 — Structured concurrency

```python
import asyncio


async def operation(name, delay):
    await asyncio.sleep(delay)
    return name


async def main():
    async with asyncio.TaskGroup() as group:
        first = group.create_task(
            operation("A", 0.05)
        )
        second = group.create_task(
            operation("B", 0.01)
        )

    assert first.result() == "A"
    assert second.result() == "B"


asyncio.run(main())
```

A task group waits for related tasks and coordinates failure and cancellation behavior.

---

## Exercise 17 — Async generator

```python
import asyncio


async def event_stream():
    for event in [
        "ticket.created",
        "ticket.classified",
        "ticket.closed",
    ]:
        await asyncio.sleep(0.01)
        yield event


async def main():
    events = []

    async for event in event_stream():
        events.append(event)

    assert events == [
        "ticket.created",
        "ticket.classified",
        "ticket.closed",
    ]


asyncio.run(main())
```

---

## Exercise 18 — Async HTTP client

Install aiohttp:

```bash
python -m pip install aiohttp
```

```python
import asyncio
import aiohttp


async def fetch(
    session,
    semaphore,
    url,
):
    async with semaphore:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return {
                    "url": url,
                    "status": response.status,
                    "text": await response.text(),
                }
        except Exception as error:
            return {
                "url": url,
                "error": str(error),
            }


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
                fetch(session, semaphore, url)
                for url in urls
            ]
        )

    for result in results:
        print(result["url"])
```

One session is reused and at most two requests enter the protected region at once.

---

## Exercise 19 — Mixed async and CPU work

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor


def calculate_score(values):
    return sum(
        value * value
        for value in values
    )


async def fetch_data():
    await asyncio.sleep(0.1)
    return list(range(100_000))


async def main():
    values = await fetch_data()
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

The CPU calculation runs in a separate process instead of blocking the event loop.

---

## Exercise 20 — Choose the appropriate tool

1. Calling 100 HTTP APIs with an async HTTP client: `asyncio`, because the work is I/O-bound and the client is already asynchronous.
2. CPU-heavy pure-Python transformation: a process pool, because separate processes can use multiple CPU cores without being limited by the normal GIL behavior.
3. Blocking third-party SDK inside an async application: a thread pool or `asyncio.to_thread()`, because the SDK blocks the event-loop thread.
4. Shared in-memory message queue: threads with `queue.Queue`, when the workers use blocking functions and share one process.
5. Independent CPU-heavy model evaluations: a process pool, unless the model library already releases the GIL and benchmarking proves threads are effective.

The choice should be confirmed by measuring the real workload.

---

## Exercise 21 — Final concurrent ticket pipeline

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor


def calculate_score(text):
    return sum(
        ord(character)
        for character in text
    ) % 100


async def retrieve_ticket(ticket_id):
    await asyncio.sleep(0.02)
    return {
        "id": ticket_id,
        "text": f"Payment issue for {ticket_id}",
    }


async def classify_ticket(
    ticket,
    semaphore,
):
    async with semaphore:
        async with asyncio.timeout(2):
            await asyncio.sleep(0.02)

            if ticket["id"] == "T-003":
                raise RuntimeError("Classifier failed")

            return {
                **ticket,
                "category": "billing",
            }


async def main():
    ticket_ids = [
        "T-001",
        "T-002",
        "T-003",
        "T-004",
    ]

    tickets = await asyncio.gather(
        *[
            retrieve_ticket(ticket_id)
            for ticket_id in ticket_ids
        ]
    )

    semaphore = asyncio.Semaphore(2)

    classification_results = await asyncio.gather(
        *[
            classify_ticket(ticket, semaphore)
            for ticket in tickets
        ],
        return_exceptions=True,
    )

    successful = [
        result
        for result in classification_results
        if isinstance(result, dict)
    ]

    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as pool:
        scored = await asyncio.gather(
            *[
                loop.run_in_executor(
                    pool,
                    calculate_score,
                    ticket["text"],
                )
                for ticket in successful
            ]
        )

    final_results = [
        {
            **ticket,
            "score": score,
        }
        for ticket, score in zip(
            successful,
            scored,
        )
    ]

    return final_results


results = asyncio.run(main())

assert len(results) == 3
assert all(
    result["category"] == "billing"
    for result in results
)
```

The failed classification is excluded while successful results continue through CPU-heavy scoring.

---

# Review checklist

You should now understand:

- The difference between concurrency and parallelism.
- Why threads are useful for blocking I/O.
- Why locks protect shared mutable state.
- How queues coordinate producers and consumers.
- How thread and process pools return futures.
- Why process workers need serializable functions and arguments.
- How the event loop schedules coroutines.
- How tasks, `gather()`, `TaskGroup`, timeouts, and cancellation work.
- Why blocking functions must not run directly in the event loop.
- How async generators stream values.
- How to limit concurrent HTTP requests.
- How to combine asyncio with a process pool.
