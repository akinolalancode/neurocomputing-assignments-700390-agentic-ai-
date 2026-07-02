# Temperature: 0.3
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

# Initialize the first two Fibonacci numbers
a, b = 0, 1

# Iterate through the Fibonacci sequence and print values less than 100
for i in range(1, 100):
    if fibonacci(i) < 100:
        print(fibonacci(i))