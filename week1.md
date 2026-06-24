Operators

In Python, **operators** are special symbols or keywords used to perform computations and manipulate data, 
acting as the functional blocks of your code. They are grouped into several types based on what they do: **arithmetic operators** 
handle math (like `+` for addition, `*` for multiplication, and `%` for finding a remainder), 
while **assignment operators** (like `=` or `+=`) store or update values in variables. You also use **comparison operators** 
(like `==` to check if values are equal or `!=` to see if they are different) to evaluate conditions, 
and **membership operators** (like `in` and `not in`) to check if a specific item exists inside a collection like a list or string. 
For example, in the expression `is_available = price < 100`, the comparison operator `<` checks the value, 
and the assignment operator `=` saves the true or false result into your variable.



a = ' me'
b = 'myself'
c = a + b
d = a + ", " + b
e = a * 3
f = "3" # as a string
g = 2 # as a integer
h = g + int(f)
i = "Car"
i[0] = 'B'  # NOTE: This will block because strings are immutable, so we will have to reassign the whole string.
i = 'B' + i[1:len(i)]


print(f'\n{c}')
print(f'\n{d}')
print(f'\n{e}')
print(f'\n{float(h)}')
print(f'\n{i}')




==================================================================

'and' and 'or' operators

In Python, `and` and `or` are logical operators used to combine multiple conditions, 
but they evaluate them using a concept called **short-circuit evaluation**. 
The `and` operator requires **all** conditions to be true, returning the first value that evaluates to false, 
or the final value if everything is true. Conversely, the `or` operator only requires **at least one** condition to be true, 
returning the very first truthy value it encounters without even looking at the rest. 
Because Python evaluates these from left to right and stops as soon as the outcome is certain, 
you can efficiently chain them together to control the flow of your code based on complex, intersecting rules.



print("0" and "apple")
print(0 and "apple")
print(0 and 3)
print(3 and 0)
print("apple" and 0)
print("apple" and "0")


print("0" or "apple")
print(0 or "apple")
print(0 or 3)
print(3 or 0)
print("apple" or 0)
print("apple" or "0")


print("apple" or 0 and 't')
print("apple" and 0 or 3)
print(True or False and False)
print(False and True or True)


print([] or {} or 'success')
True and print('Step 1') or print("Step 2")
print([0] and {1} or (2,))
print([[]] and [0] or {})
print('A') or print('B') and print('C') or 'Final'


def lower_bound():
    print('Low')
    return 10
def upper_bound():
    print('High')
    return 20
result = lower_bound() > 15 and upper_bound() < 30
