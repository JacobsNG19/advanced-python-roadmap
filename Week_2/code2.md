**A Class That Stores Weights and a Bias**

We examine a class that holds a list of numbers together with one extra number, then performs a calculation when asked.

```python
class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def forward(self, inputs):
        total = 0
        for weight, value in zip(self.weights, inputs):
            total += weight * value
        total += self.bias
        return total
```

**What the pieces mean**

- `zip` walks the two lists side by side and pairs each weight with its corresponding input.  
- The loop multiplies every pair and accumulates the products.  
- The bias is added once at the end so the result may sit above or below zero.

**Working example**

```python
n = Neuron([0.5, -0.2, 0.1], 0.3)
result = n.forward([1.0, 2.0, 3.0])
print(result)   # 0.7
```

**What we keep in mind**

- An attribute may hold a list just as easily as a single number.  
- A method can receive another list and combine it with the object’s own data.  
- Keeping the stored values separate from the calculation makes the class easy to reuse.


**A More Careful Version**

We strengthen the method so that it refuses to work when the lists differ in length.

```python
class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def forward(self, inputs):
        if len(self.weights) != len(inputs):
            return None

        total = 0
        for weight, value in zip(self.weights, inputs):
            total += weight * value
        total += self.bias
        return total
```

**What we have gained**

- The method now accepts any length, provided both lists match.  
- A clear check prevents silent errors.  
- The calculation stays inside the method; the decision to use or display the result stays outside.

**One improvement worth considering**

Returning `None` is correct, yet every caller must then test for `None`.  
Raising a `ValueError` with a short message would tell the caller exactly what went wrong and leave the recovery decision in the caller’s hands.

**Question we may ask**

What is the practical difference between returning `None` and raising an exception?  
When does each choice serve the larger program better?

**Next small step**

Add a second method called `forward_non_negative` that:

1. Calls the ordinary `forward` method.  
2. Returns the result only when it is greater than zero.  
3. Returns zero when the result is zero or negative.

This leaves the original method pure while giving a convenient way to refuse negative results when they are not wanted.

**Small Practice**

Create one neuron, call both methods with matching lists, then call them again with mismatched lists and observe the different outcomes.
