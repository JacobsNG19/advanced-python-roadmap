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


**A More Careful Calculator**

We now strengthen the class so that it refuses to work when the lists do not match in length.

```python
class Calculator:
    def __init__(self, factors, offset):
        self.factors = factors
        self.offset = offset

    def compute(self, values):
        if len(self.factors) != len(values):
            return None

        total = 0
        for factor, value in zip(self.factors, values):
            total += factor * value
        total += self.offset
        return total
```

**What we have done well**

- The method now works for any number of values, provided the lengths agree.  
- A clear check prevents silent mistakes when the lists are mismatched.  
- The calculation remains inside the method; the decision to print or use the result stays outside.  
- Variable names stay plain and honest.

**One subtle improvement to consider**

Returning `None` is correct, yet it forces every caller to test for `None`.  

Raising a `ValueError` with a short, descriptive message would tell the caller exactly what went wrong and leave the decision about how to recover in the caller’s hands.

**Question we may ask ourselves**

What is the practical difference between returning `None` and raising an exception?  
When does each choice serve the larger program better?

**Next small step**

Add a second method called `compute_positive` that:

1. Calls the ordinary `compute` method.  
2. Returns the result only when it is greater than zero.  
3. Returns zero when the result is zero or negative.

This keeps the original method pure and gives us a convenient way to refuse negative totals when they make no sense.

**Small Practice**

Create a calculator, call both methods with matching lists, then call them again with mismatched lists and observe the different outcomes.

---

**Real-world exercise**

Design a ShippingCost class that stores a list of distance rates and a fixed handling fee.  
Add a method that receives a list of package weights, multiplies each weight by its corresponding rate, adds the handling fee, and returns the total.  
If the number of rates does not match the number of weights, the method must refuse to calculate.  
Create one shipping-cost object and test it with both matching and mismatched lists.