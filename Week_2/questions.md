1. Design a ShippingCost class that holds a list of distance rates and a fixed handling fee. Add a method that receives a list of package weights, multiplies each weight by its corresponding rate, adds the handling fee, and returns the total cost. Create one shipping-cost object and calculate the price for a small set of packages.

2. Why do we raise a `ValueError` when the length of the weights does not match the length of the inputs, instead of simply returning `None`?
 
3. In the `forward` method, after we finish the loop and add the bias, why do we pass the total through `relu` before returning it?
 
4. What does the `set_weights` method need to check before it replaces the existing weights, and why is that check important?

5. If we create a neuron with weights `[0.5, -0.2, 0.1]` and bias `0.3`, then call `forward` with `[1.0, 2.0, 3.0]`, what is the final result and why does `relu` leave that result unchanged?