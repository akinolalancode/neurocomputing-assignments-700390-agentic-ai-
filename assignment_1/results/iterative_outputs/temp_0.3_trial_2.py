# Temperature: 0.3
# Top-p: 0.95
# Executable: True
# Correct: False
# Exact Match: False

def fibonacci_sequence():
    fib_sequence = []
    a, b = 0, 1
    while a < 100:
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

# Get the Fibonacci sequence
fib_sequence = fibonacci_sequence()

# Print all Fibonacci numbers less than 100
print("Fibonacci sequence less than 100:")
for num in fib_sequence:
    print(num)