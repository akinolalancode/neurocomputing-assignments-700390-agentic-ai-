# Temperature: 0.5
# Top-p: 0.95
# Executable: True
# Correct: False
# Exact Match: False

def fibonacci(n):
    # Base case: the first two Fibonacci numbers are 0 and 1
    if n <= 1:
        return n
    else:
        # Recursive case: sum of the two preceding Fibonacci numbers
        return fibonacci(n - 1) + fibonacci(n - 2)

# Print all Fibonacci numbers less than 100
for i in range(100):
    if fibonacci(i) < 100:
        print(fibonacci(i))