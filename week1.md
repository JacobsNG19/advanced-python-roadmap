a = ' me'
b = 'myself'

# String Concatenation & Repetition
c = a + b
d = a + ", " + b
e = a * 3

# Type Casting (Converting string to integer)
f = "3"         # defined as a string
g = 2           # defined as an integer
h = g + int(f)  # converts "3" to 3, then adds 2

# String Immutability Handling
i = "Car"
# i[0] = 'B'  <-- This throws a TypeError because strings cannot be mutated.
# Instead, we rebuild the string using slicing:
i = 'B' + i[1:len(i)]

# Outputs
print(f'c: {c}')
print(f'd: {d}')
print(f'e: {e}')
print(f'h (as float): {float(h)}')
print(f'i: {i}')
