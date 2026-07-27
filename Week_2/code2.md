**A Class That Computes a Weighted Sum**

We now examine a class that stores a list of numbers together with a single extra number, then performs a calculation when asked.

```python
class Calculator:
    def __init__(self, factors, offset):
        self.factors = factors   # a list of numbers
        self.offset = offset     # a single number

    def compute(self, values):
        total = 0
        for factor, value in zip(self.factors, values):
            total += factor * value
        total += self.offset
        return total
```

**What the pieces mean**

- `zip(self.factors, values)` walks through the two lists side by side, pairing each factor with its matching value.  
- The loop multiplies each pair and adds the product to a running total.  
- The offset is added once at the end. Without it the result would always pass through the origin; the offset lets the result shift up or down freely.

**Working example**

```python
calc = Calculator([0.5, -0.2, 0.1], 0.3)
result = calc.compute([1.0, 2.0, 3.0])
print(result)   # 0.7
```

**What we keep in mind**

- Attributes can hold lists as easily as single numbers.  
- A method may receive another list and combine it with the object’s own data.  
- Clear separation of stored data and calculation keeps the class easy to reuse.

**Small Practice**

Create a second calculator with different factors and offset, then call `compute` with a new list of values and observe the independent result.
