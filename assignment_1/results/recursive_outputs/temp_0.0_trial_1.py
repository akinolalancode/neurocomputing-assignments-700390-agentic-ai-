# Temperature: 0.0
# Top-p: 0.95
# Executable: True
# Correct: False
# Exact Match: False

def fibonacci(n):
    # Base case: if n is 0 or 1, return n
    if n == 0 or n == 1:
        return n
    # Recursive case: return the sum of the two preceding Fibonacci numbers
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# Initialize the first two Fibonacci numbers
fib_sequence = [0, 1]

# Print the first two Fibonacci numbers
print("Fibonacci sequence:", fib_sequence)

# Calculate and print Fibonacci numbers less than 100
for i in range(2, 100):
    if fibonacci(i) < 100:
        print(f"Fibonacci({i}) = {fibonacci(i)}")