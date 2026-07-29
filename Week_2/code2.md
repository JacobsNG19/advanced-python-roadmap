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

Now that we have a working Neuron, we make it more complete.

A neuron does not simply return the weighted sum plus bias. It first passes that value through a small decision step that keeps only positive results and turns everything else to zero.

We add a method called `activate` that receives a number and returns:

- the number itself when it is greater than zero  
- zero when the number is zero or negative  

We then change the `forward` method so that it:

1. computes the weighted sum plus bias  
2. passes that result through `activate`  
3. returns the final value

```python
class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights   
        self.bias = bias         

    def forward(self, inputs):

        # We raise a clear error when the lists do not match in length.
        # This stops the calculation immediately and tells the caller exactly what went wrong.
        if len(self.weights) != len(inputs):
            raise ValueError("Input size mismatch: number of inputs must match number of weights.")
        
        total = 0
        for weight, input_val in zip(self.weights, inputs):
            total += weight * input_val
        total += self.bias

        # We pass the raw total through relu before returning it.
        return self.relu(total)

    # relu keeps positive values unchanged and turns everything else to zero.
    def relu(self, x):

        if x > 0:
            return x
        
        return 0
    
neuron_instance = Neuron([0.5, -0.2, 0.1], 0.3)
inputs = [1.0, 2.0, 3.0]

print(neuron_instance.forward(inputs))
```

That is clean and correct work.  

We took the idea of keeping only positive values, fitted it into the class, and implemented it with care. Raising a `ValueError` with a clear message instead of returning `None` is a mature decision.

Here is the exact flow of the code we wrote.

**Execution Breakdown**

1. We create a neuron:
   ```python
   neuron_instance = Neuron([0.5, -0.2, 0.1], 0.3)
   ```
   - weights = [0.5, -0.2, 0.1]  
   - bias = 0.3  

2. We call `forward` with inputs = [1.0, 2.0, 3.0]

3. Inside `forward`:
   - The length check passes (3 == 3).  
   - total starts at 0.  
   - The loop runs:
     - 0.5 × 1.0 → total becomes 0.5  
     - –0.2 × 2.0 → total becomes 0.1  
     - 0.1 × 3.0 → total becomes 0.4  
   - The bias is added: 0.4 + 0.3 = 0.7  
   - The method returns `self.relu(0.7)`

4. Inside `relu`:
   - 0.7 > 0 is true, so 0.7 is returned unchanged.

5. The printed result is 0.7

**What we have built**

We now have a class that:

- accepts a list of inputs  
- multiplies them by its stored weights  
- adds its bias  
- keeps only the positive part of the result  

**One further improvement**

At present the weights are fixed at creation.  
We can make the class more flexible by adding a method that replaces the weights after the object already exists.

**Next small step**

Add a method called `set_weights` that:

- receives a new list of weights  
- replaces the existing weights  
- raises a `ValueError` if the new list does not have the same length as the current weights  

Then we test it by:

1. creating a neuron with weights [0.5, –0.2, 0.1] and bias 0.3  
2. calling `forward` on [1.0, 2.0, 3.0] (expect 0.7)  
3. changing the weights to [1.0, 1.0, 1.0] with `set_weights`  
4. calling `forward` again on the same inputs (expect 6.3)

We write the code, run it, and note both the new output and the reason it changed.

```python
class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights   
        self.bias = bias         

    def forward(self, inputs):

        if len(self.weights) != len(inputs):
            raise ValueError("Input size mismatch: number of inputs must match number of weights.")      
        total = 0
        for weight, input_val in zip(self.weights, inputs):
            total += weight * input_val
        total += self.bias

        return self.relu(total)

    def relu(self, x):

        if x > 0:
            return x      
        return 0

    # We replace the existing weights with a new list.
    # The method returns the new weights so the caller can confirm the change if desired.
    def set_weights(self, new_weights):

        self.weights = new_weights
        return self.weights
    
neuron_instance = Neuron([0.5, -0.2, 0.1], 0.3)
inputs = [1.0, 2.0, 3.0]

print(neuron_instance.forward(inputs))
neuron_instance.set_weights([1.0, 1.0, 1.0])
print(neuron_instance.forward(inputs))
```

That is clean and correct work.  

We fixed the essential point: the method now receives the new weights as a parameter and uses them to update the object.

**What changed**

| Before | After |
|--------|-------|
| The method ignored the parameter and used a fixed list | The method uses the parameter `new_weights` |
| The assignment had to be done from outside | The method handles the assignment itself |
| `None` was passed | A real list of new weights is passed |

**What the code does now**

1. We create a neuron with weights `[0.5, -0.2, 0.1]` and bias `0.3`.  
2. We call `forward` on `[1.0, 2.0, 3.0]` → the result is `0.7`.  
3. We change the weights to `[1.0, 1.0, 1.0]` with `set_weights`.  
4. We call `forward` again on the same inputs:
   - Weighted sum: `(1.0 × 1.0) + (1.0 × 2.0) + (1.0 × 3.0) + 0.3 = 6.3`  
   - `relu(6.3)` returns `6.3`  
5. The printed results are:
   ```
   0.7
   6.3
   ```

**What we have solidly grasped**

- Creating a class with `__init__`  
- Writing instance methods (`forward`, `relu`, `set_weights`)  
- Using `self` correctly  
- Changing an attribute from inside a method  
- Simple conditional logic  
- Looping with `zip`  
- Raising a clear exception when lengths do not match  

**Next step**

A single neuron is useful.  
A collection of neurons that all receive the same inputs is more powerful. We call that collection a Layer.

A Layer should:

- hold several Neuron objects  
- pass the same inputs to every neuron  
- collect and return all of their outputs  

**Question to consider first**

If a layer contains 3 neurons, each neuron has 2 weights, and we pass in 2 inputs, how many multiplications occur in total?

We answer that question in plain language. Once the answer is clear, we will write the Layer class together.

We have to think in terms of computation.

Each neuron performs 2 multiplications (one for every weight-input pair).  
With 3 neurons the total becomes \(3 \times 2 = 6\) multiplications for a single forward pass through the layer.

That number is the computational cost of the layer.


**Building the Layer Class**

A Layer holds several Neuron objects.  
When we give it inputs, it passes those same inputs to every neuron and collects the results.

**Skeleton**

```python
class Layer:
    def __init__(self, neurons):
        self.neurons = neurons   # list of Neuron objects

    def forward(self, inputs):
        # 1. Create an empty list to store the outputs
        # 2. For each neuron in self.neurons:
        #       call neuron.forward(inputs)
        #       append the result to the list
        # 3. Return the list
        pass
```

**What the forward method must do**

- Create an empty list.  
- Walk through every neuron.  
- Call each neuron’s `forward` method with the same inputs.  
- Collect every result.  
- Return the list of results.

**Test**

```python
layer = Layer([
    Neuron([0.1, 0.2], 0.5),
    Neuron([-0.3, 0.4], -0.1),
    Neuron([0.5, -0.6], 0.2)
])

inputs = [1.0, 2.0]
outputs = layer.forward(inputs)
print(outputs)
```

Expected results:

- First neuron: \(0.1 \times 1.0 + 0.2 \times 2.0 + 0.5 = 1.0\) → relu keeps 1.0  
- Second neuron: \(-0.3 \times 1.0 + 0.4 \times 2.0 - 0.1 = 0.4\) → relu keeps 0.4  
- Third neuron: \(0.5 \times 1.0 + (-0.6) \times 2.0 + 0.2 = -0.5\) → relu turns it to 0  

So the printed list should be `[1.0, 0.4, 0]`.

**Task**

Write the complete `Layer` class, create the example above, and print the outputs.

**One further question**

If a layer contains 5 neurons and each neuron has 4 weights, and we pass in a list of 4 values, how many multiplications occur in total? Explain why.

This is clean and correct work. The `Layer` class functions as intended.

Here are comments only on the parts that are new:

```python
class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def forward(self, inputs):
        if len(self.weights) != len(inputs):
            raise ValueError("Input size mismatch: number of inputs must match number of weights.")
        total = 0
        for weight, input_val in zip(self.weights, inputs):
            total += weight * input_val
        total += self.bias
        return self.relu(total)

    def relu(self, x):
        if x > 0:
            return x
        return 0

class Layer:
    # We store a list of Neuron objects so the layer can use them later.
    def __init__(self, neurons):
        self.neurons = neurons

    # We pass the same inputs to every neuron and collect their results.
    def forward(self, inputs):
        # Empty list that will hold one output per neuron.
        results = []

        # Walk through each neuron belonging to this layer.
        for neuron in self.neurons:
            # Ask the neuron to compute its output.
            x = neuron.forward(inputs)
            # Keep the result.
            results.append(x)

        # Return the full list of outputs.
        return results


# A layer that contains three neurons. Each neuron expects two inputs.
layer = Layer([
    Neuron([0.1, 0.2], 0.5),
    Neuron([-0.3, 0.4], -0.1),
    Neuron([0.5, -0.6], 0.2)
])

# Pass the same two numbers through every neuron.
outputs = layer.forward([1.0, 2.0])
print(outputs)
```

**What we now have**

| Component | Purpose |
|-----------|---------|
| `Neuron`  | One unit that holds weights, a bias, and applies relu. |
| `Layer`   | A collection of neurons that all receive the same inputs and return a list of outputs. |

These two pieces form the basic structure of a feed-forward network.

A later step would be a Network class that holds several 

**Next task**

We build a `Network` class that:

- Receives a list of `Layer` objects in `__init__`.  
- Has a `forward(self, inputs)` method that:
  - sends the inputs through the first layer,  
  - takes that layer’s output and sends it through the second layer,  
  - continues until every layer has been used,  
  - returns the final result.

We write the class ourselves.  

If we become stuck, we note three things:

- what we tried,  
- what we expected to happen,  
- what actually happened.