### Phase 1: Basics, Strings, & Branching (Intermediate)

#### Q1: Short-Circuit Evaluation

What does the following snippet return, and why doesn't it throw a `ZeroDivisionError`?

Python

```
x = 0
result = (x == 0) or (10 / x == 2)
print(result)
```

> [!hint] + Hint
> 
> Look into how Python's logical operators (`or`, `and`) evaluate expressions from left to right.

#### Q2: String Immutability & Memory

If strings in Python are immutable, what actually happens in memory when you execute the code below? Is it efficient for large-scale loops?

Python

```
s = "Rolls"
s += " Royce"
```

> [!hint] + Hint
> 
> Python has to create a brand-new string object in memory every time you concatenate. Think about the implications of this inside a loop of 1 million iterations.

#### Q3: Negative Indexing & Slicing Step

Given `s = "Python"`, what is the output of `s[::-2]`? Explain how the start, stop, and step parameters behave when the step is negative.

> [!hint] + Hint
> 
> When the step is negative, Python slices backward. The default start and stop positions swap roles.

#### Q4: The `input()` Trap

If a user inputs the number `42` into the following code, why will it raise a `TypeError`? How do you fix it?

Python

```
age = input("Enter your age: ")
if age > 18:
    print("Adult")
```

> [!hint] + Hint
> 
> Check the default return type of the built-in `input()` function.

#### Q5: Chained Comparisons

How does Python interpret the expression `1 < x < 3` dynamically? Does it evaluate `1 < x` first and compare the boolean result to `3`?

> [!hint] + Hint
> 
> Python transforms chained comparisons using an implicit logical operator. It behaves like `(1 < x) and ...`.

### Phase 2: Iteration & Guess-and-Check (Intermediate-Plus)

#### Q6: Loop `else` Clause

What is the purpose of the `else` block in a `for` or `while` loop, and when exactly does it execute?

Python

```
for i in range(3):
    if i == 5:
        break
else:
    print("Loop finished normally!")
```

> [!hint] + Hint
> 
> The `else` block runs _only if_ the loop completes all iterations without encountering a specific control flow statement.

#### Q7: Modifying a Collection While Iterating

Why is it dangerous to delete items from a list while iterating over it using a standard `for` loop? What happens to the internal index?

> [!hint] + Hint
> 
> Python's `for` loop keeps track of the current index. If you remove an element, the list shrinks, skipping the next item.

#### Q8: Guess-and-Check (Exhaustive Enumeration)

Write a small Python snippet using exhaustive enumeration to find the cube root of a perfect cube integer entered by the user. If it's not a perfect cube, print an error message.

> [!hint] + Hint
> 
> Start a counter at `0`, cube it, and increment it until its cube is greater than or equal to the absolute value of the input.

### Phase 3: Binary, Floats, & Approximation (Advanced-Intermediate)

#### Q9: Floating-Point Inexactness

Why does `0.1 + 0.2 == 0.3` evaluate to `False` in Python?

> [!hint] + Hint
> 
> Computers represent floating-point numbers in binary (base 2). Think about trying to write $1/3$accurately in base 10 decimals ($0.3333...$).

#### Q10: Epsilon ($\epsilon$) in Approximation

When implementing an approximation method (like finding a square root), why do we use `abs(guess2 - x) < epsilon` instead of `guess2 == x`?

> [!hint] + Hint
> 
> Because floating-point steps might skip the exact answer entirely due to precision limits. We look for an answer that is "close enough".

#### Q11: Bisection Search Mechanics

Suppose you are searching for the square root of a number $x$ where $0 < x < 1$ (e.g., $x = 0.25$) using bisection search. Why does setting your initial upper bound to $x$ fail, and how do you fix it?

> [!hint] + Hint
> 
> The square root of a fraction between $0$ and $1$ is always _larger_ than the number itself (e.g., $\sqrt{0.25} = 0.5$).

#### Q12: Underflow vs. Overflow

What happens when a floating-point calculation in Python results in a number too close to zero to be represented? What happens if it's too large?

> [!hint] + Hint
> 
> One scenario scales down to `0.0` (underflow), while the other scales up to `inf` (overflow) without necessarily crashing your program.

### Phase 4: Decomposition, Abstractions, & Functions (Advanced)

#### Q13: Variable Scope (LEGB Rule)

Explain the output of the following code. Which scope rule allows `inner` to read `x`, and why does changing `x`inside `inner` require special keywords?

Python

```
def outer():
    x = "local"
    def inner():
        print(x)
    inner()
outer()
```

> [!hint] + Hint
> 
> Python searches names using the LEGB hierarchy: **L**ocal, **E**nclosing, **G**lobal, **B**uilt-in.

#### Q14: Mutable Default Arguments

Predict the output of calling `add_item(1)` twice in a row. Why does this behavior occur?

Python

```
def add_item(val, my_list=[]):
    my_list.append(val)
    return my_list
```

> [!hint] + Hint
> 
> Python evaluates default arguments _once_ when the function is defined, not every time the function is called.

#### Q15: Docstrings and Structural Abstraction

What is the structural difference between a comment (`#`) and a docstring (`"""..."""`) regarding Python code abstraction, and how can a developer access a function's docstring programmatically at runtime?

> [!hint] + Hint
> 
> Docstrings are stored as metadata on the function object. Look up the `__doc__` attribute or the `help()` function.

#### Q16: Positional-Only vs. Keyword-Only Arguments

In the function signature below, what do the `/` and `*` syntaxes enforce?

Python

```
def process_data(a, /, b, *, c):
    pass
```

> [!hint] + Hint
> 
> Arguments before `/` must be positional. Arguments after `*` must be explicitly named (keywords).

#### Q17: `*args` and `kwargs` Unpacking

Write a function `multiply_and_log(prefix, *args)` that takes a string `prefix` and an arbitrary number of numbers, multiplies all the numbers together, and prints the prefix followed by the result.

> [!hint] + Hint
> 
> `*args` captures all remaining positional arguments into a tuple. You can iterate over this tuple.

#### Q18: Pass-by-Object-Reference

Python is said to use "pass-by-object-reference" (or pass-by-assignment). If you pass a list to a function and reassign the list inside the function (`lst = [1, 2]`), does it change the original list outside? What if you mutate it (`lst.append(1)`)?

> [!hint] + Hint
> 
> Reassigning binds the local variable name to a brand-new object. Modifying alters the existing object that both the internal and external names point to.

### Phase 5: Functions as First-Class Objects (Advanced Master)

#### Q19: Higher-Order Functions

Write a function `apply_twice(f, x)` that takes a function `f` and an argument `x`, and returns `f(f(x))`. Test it by passing a lambda function that squares a number.

> [!hint] + Hint
> 
> Treat `f` just like any variable—you can invoke it using parentheses: `f(...)`.

#### Q20: Functions in Data Structures

How can you store functions inside a dictionary to replace a massive, messy `if-elif-else` branching statement? Show a quick conceptual example for basic math operations (`+`, `-`).

> [!hint] + Hint
> 
> Maps keys like `"+"` directly to the function objects (like `operator.add` or lambda functions), then look them up and invoke them: `ops[key](a, b)`.

#### Q21: Closures

What is a closure? Explain how the inner function below retains access to `multiplier` even after `make_multiplier`has completely finished executing.

Python

```
def make_multiplier(multiplier):
    def multiply(x):
        return x * multiplier
    return multiply

times3 = make_multiplier(3)
print(times3(10))
```

> [!hint] + Hint
> 
> The inner function encloses the environmental variables from its parent scope at the time it was created.

#### Q22: Lambda Functions Limits

What are the syntax limitations of a `lambda` function in Python compared to a standard `def` block? Can you use loops or multiple expressions inside a `lambda`?

> [!hint] + Hint
> 
> Lambdas are restricted to a single, implicit-return expression. They cannot contain statements like `for`, `while`, or assignment statements (`=`).

#### Q23: The `map()` and `filter()` Abstractions

How do `map()` and `filter()` take advantage of functions as first-class objects? What type of object do they return, and why doesn't it instantly compute the values?

> [!hint] + Hint
> 
> They return lazy iterators. They don't compute elements until you explicitly ask for them (e.g., by wrapping them in a `list()`).

#### Q24: Function Attributes

Since functions are objects, you can assign custom attributes to them. How can you use a function attribute to track how many times a specific function has been called?

Python

```
def my_func():
    pass # Track calls here
```

> [!hint] + Hint
> 
> You can initialize and increment a variable directly on the function name, such as `my_func.counter = 0`.

#### Q25: The Ultimate Synthesis (Bisection with Functions)

Write a function `find_root(f, low, high, epsilon)` that uses **bisection search** to find the root of _any_ arbitrary continuous mathematical function `f` passed into it (where $f(x) = 0$).

> [!hint] + Hint
> 
> Combine Phase 3 and Phase 5. Evaluate the function inside your search loop by calling `f(mid)`. Use the sign of `f(mid)` to determine whether to move your `low` or `high` bounds.

### Phase 6: Deep Strings, Indexing, and Memory (Advanced)

#### Q26: String Interning and Object Identity

Predict the output of the following identity checks (`is`). Why does Python give different results for these seemingly identical operations?

Python

```
a = "hello"
b = "hello"
print(a is b)

c = "hello world!"
d = "hello world!"
print(c is d)
```

> [!hint] + Hint
> 
> Research **String Interning** in CPython. Python automatically optimizes memory for short string literals that look like identifiers, but doesn't do it for all strings at runtime.

#### Q27: Slicing Memory Overhead

When you take a large slice of a string (e.g., `large_string[1000:5000]`), does Python copy the characters into a new memory location, or does it point back to the original string? What is the Space Complexity $O(N)$ of string slicing?

> [!hint] + Hint
> 
> Python strings are immutable, but slicing them still creates a brand-new string object containing a _copy_ of the data. For memory-mapped or zero-copy slicing, one must look into `memoryview`objects.

#### Q28: String Building Optimization

Why is `''.join(list_of_strings)` asymptotically faster ($O(N)$) than using a `for` loop with `+=` string concatenation ($O(N^2)$)? Explain what happens to memory allocation during both processes.

> [!hint] + Hint
> 
> With `+=`, Python has to repeatedly reallocate memory and copy the old string into a new one. With `.join()`, Python calculates the total memory required _first_, allocating it all in a single pass.

#### Q29: Complex Multi-Step Slicing Bounds

Given `s = "Computational"`, what does `s[2:10:-2]` return? Explain how Python evaluates a slice when the bounds and the step direction conflict.

> [!hint] + Hint
> 
> Look at the direction. If `start < stop` but the step is negative, Python cannot traverse backwards from 2 to 10. It will return an empty collection without throwing an error.

### Phase 7: Advanced Branching, Iteration, and Control Flow

#### Q30: Short-Circuiting with Side Effects

If you pass functions with side effects (like printing or mutating variables) into a complex conditional block, what is the exact execution order? Predict the output:

Python

```
def check_a():
    print("A")
    return False

def check_b():
    print("B")
    return True

if check_a() and check_b():
    print("Success")
```

> [!hint] + Hint
> 
> Because of short-circuit evaluation, if `check_a()` evaluates to `False`, the `and` statement is already guaranteed to fail. Python completely skips executing `check_b()`.

#### Q31: The Iteration Protocol Mechanics

When you write `for char in "MIT":`, what is Python actually doing under the hood? Explain the roles of the hidden `iter()` and `next()` built-in functions, and how the loop knows when to stop.

> [!hint] + Hint
> 
> The `for` loop calls `iter()` on the sequence to get an iterator object. It then calls `next()` repeatedly until the iterator raises a `StopIteration` exception, which the loop catches internally to exit gracefully.

#### Q32: Sentinel-Based `while` Loops vs. Infinite Loops

When processing user inputs or network streams, why is a `while True:` loop paired with an internal `break`structurally cleaner than setting a flag variable like `running = True` and updating it at the end of the block?

> [!hint] + Hint
> 
> Using a flag variable often forces you to process data _after_ the sentinel exit condition has already been met, or requires redundant checks. `while True` with an immediate `break` stops execution exactly at the evaluation point.

### Phase 8: Floating-Point Architecture and Binary Representation

#### Q33: The Binary Fraction Limitation

Convert the decimal fraction $0.625$ into binary. Then attempt to convert $0.1$ into binary. Why can one be represented perfectly in base-2 floating-point format while the other results in an infinite repeating fraction?

> [!hint] + Hint
> 
> Any decimal fraction whose denominator can be expressed as a power of 2 ($2^n$) can be perfectly represented in binary. $0.625 = 5/8$, which is $5/2^3$. $0.1 = 1/10$, and 10 is not a power of 2.

#### Q34: Accumulation Errors in Floats

If you add `0.1` together 1,000,000 times in a loop, will the final answer be exactly `100000.0`? Explain how tiny approximation errors scale over high-iteration mathematical loops.

> [!hint] + Hint
> 
> The tiny error introduced by the binary approximation of `0.1` compounds with every single addition, leading to a significant drift in the final result.

#### Q35: IEEE 754 Special Values (`NaN` and `Inf`)

What happens when you execute `float('inf') - float('inf')` or `float('nan') == float('nan')` in Python? Explain the unusual properties of `Not-a-Number (NaN)`.

> [!hint] + Hint
> 
> Infinity minus infinity is statistically undefined, returning `nan`. Crucially, `NaN` is designed by IEEE standards to never equal anything—not even itself.

#### Q36: Arbitrary Precision Alternatives

When absolute numerical precision is mandatory (such as in financial transaction code), why are standard Python floats banned, and what built-in Python module should you substitute to fix the issue?

> [!hint] + Hint
> 
> You should use the `decimal` module (specifically `decimal.Decimal`), which represents numbers in base-10 rather than base-2, eliminating binary rounding discrepancies.

### Phase 9: Mathematical Scaling (Approximation vs. Bisection)

#### Q37: Algorithmic Efficiency: Guess-and-Check vs. Bisection

If you are looking for an answer within a search space of $N$ elements with an error margin of $\epsilon$, express the time complexity (number of steps) of a Guess-and-Check algorithm versus a Bisection Search algorithm using Big-O notation or general scaling trends.

> [!hint] + Hint
> 
> Guess-and-check scales linearly ($O(N)$) because it increments by a static step size. Bisection search cuts the remaining search space in half each step, scaling logarithmically ($O(\log N)$).

#### Q38: Bisection Search with Extreme Slopes

When using bisection search to find the root of a function $f(x) = 0$, what happens to the convergence speed if the function is nearly flat ($f'(x) \approx 0$) around the root versus when it is extremely steep?

> [!hint] + Hint
> 
> Bisection search is purely dependent on interval halving, meaning its convergence rate is entirely geometric and independent of the function's derivative or slope! (Unlike Newton-Raphson).

#### Q39: The Bisection Zero-Crossing Problem

If a function $f(x)$ approaches zero but never crosses the x-axis (e.g., $f(x) = x^2$, which touches $0$ at $x=0$ but remains positive on both sides), why will standard bisection search fail, and how do you diagnose this condition?

> [!hint] + Hint
> 
> Bisection search relies on checking if $f(\text{low})$ and $f(\text{high})$ have opposite signs ($f(\text{low}) \cdot f(\text{high}) < 0$). If the signs are identical, the algorithm cannot determine which half contains the root.

### Phase 10: Deep Decomposition, Scope, and Function States

#### Q40: Advanced LEGB Scope Leakage

Look at the code below. Why is `item` still accessible outside of the loop, and what does it print? Does Python isolate loop variable scopes?

Python

```
for item in range(5):
    pass
print("Last item:", item)
```

> [!hint] + Hint
> 
> Python does _not_ create a new local scope for `for` loops or `if` blocks. Variables bound inside a loop leak directly into the surrounding function or global scope.

#### Q41: Mutating Nonlocal Variables

How can an inner nested function modify a variable belonging to an outer function's local scope without making it a global variable? Provide the syntax.

Python

```
def counter():
    count = 0
    def increment():
        # Modify count here
        pass
```

> [!hint] + Hint
> 
> Use the `nonlocal` keyword inside the nested function. This tells Python to look in the nearest enclosing parent scope instead of creating a new local variable.

#### Q42: The Argument Unpacking Explode Pattern

What is the difference between passing data into a function using `process(*my_list)` versus `process(my_list)`? Explain the mechanism of argument unpacking.

> [!hint] + Hint
> 
> `process(my_list)` sends the entire list object as a single parameter. `process(*my_list)` extracts every element of the list and passes them in as individual, separate positional arguments.

#### Q43: Simulating Switch/Case via Functions as Objects

Before structural pattern matching was added to Python, developers used dictionaries of functions as a design pattern. Write a functional dictionary where entering `"square"` maps to a function that squares a number, and `"cube"` maps to a function that cubes it. Show how you would execute it.

> [!hint] + Hint
> 
> Define your mapping like `actions = {"square": lambda x: x**2, "cube": lambda x: x**3}`. Call it via `actions[choice](value)`.

### Phase 11: High-Level Functional Abstraction (Master Level)

#### Q44: State Retention via Closures

Closures can completely replace simple single-method objects. Write a function `make_accumulator(start_value)` that returns an inner function. Every time you call that inner function with a number, it adds that number to `start_value` and returns the new running total.

> [!hint] + Hint
> 
> You will need to use the `nonlocal` keyword inside your inner function to safely update the `start_value` stored in the parent scope.

#### Q45: Function Decorator Foundations

Since functions can accept functions as arguments and return functions as objects, write a function called `logger(f)` that wraps _any_ mathematical function `f(x)`. When the wrapped function runs, it must print `"Executing..."` before returning the actual result of `f(x)`.

Python

```
def logger(f):
    # Your code here
    pass

@logger
def square(x):
    return x * x
```

> [!hint] + Hint
> 
> Inside `logger`, define an `inner(*args, **kwargs)` function that prints the log statement, calls `f(*args, **kwargs)`, and returns that result. Then, have `logger` return the `inner` function object.

#### Q46: Delayed Evaluation via Lambdas

Explain how passing a lambda expression `lambda: heavy_computation()` into a function allows you to implement "lazy evaluation" (preventing the heavy computation from running unless it is absolutely necessary).

> [!hint] + Hint
> 
> Wrapping code in a `lambda` creates a function object without running the code block inside it. The computation is deferred until your program explicitly invokes it with parentheses `()`.

#### Q47: Passing Math Predicates to Filter Methods

Write a higher-order function `custom_filter(predicate_func, processing_list)` that replicates Python's built-in `filter()`. It should evaluate every element in `processing_list` against `predicate_func` (which returns `True` or `False`) and return a new list containing only the valid items. Do not use the built-in `filter` function.

> [!hint] + Hint
> 
> Loop through the list, execute `if predicate_func(item):`, and append matching elements to a results list.

#### Q48: Inspecting Function Objects (`__code__`)

Every Python function object contains an underlying code object accessible via `func.__code__`. What kind of metadata is stored here, and how does it help Python run your abstractions?

> [!hint] + Hint
> 
> It holds critical compiler architecture details, such as variable names used inside the function (`co_varnames`), constants (`co_consts`), and the total number of expected positional arguments.

#### Q49: Abstract Mathematical Composition

Write a higher-order function `compose(f, g)` that takes two functions as arguments and returns a new function representing their mathematical composition, $f(g(x))$.

> [!hint] + Hint
> 
> Your outer function returns an inner function: `return lambda x: f(g(x))`.

#### Q50: The Ultimate Meta-Programming Boundary

Can a function in Python modify its _own_ default arguments dynamically after it has already been defined? If so, where are those default values hidden inside the function object?

> [!hint] + Hint
> 
> Yes! Default values for positional-or-keyword arguments are stored as a mutable tuple in the function's internal `__defaults__` attribute, which can be modified at runtime.
