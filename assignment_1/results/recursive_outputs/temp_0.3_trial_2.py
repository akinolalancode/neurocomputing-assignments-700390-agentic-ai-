# Temperature: 0.3
# Top-p: 0.95
# Executable: True
# Correct: False
# Exact Match: False

def fibonacci(n):
    # Base case: if n is 0 or 1, return n itself
    if n == 0 or n == 1:
        return n
    # Recursive case: sum of the two preceding Fibonacci numbers
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# Initialize the first two Fibonacci numbers
fib_sequence = [0, 1]

# Print all Fibonacci numbers less than 100
for i in range(2, 100):
    if fibonacci(i) < 100:
        print(fibonacci(i))