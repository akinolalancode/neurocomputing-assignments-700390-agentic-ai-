# Temperature: 0.7
# Top-p: 0.95
# Executable: True
# Correct: False
# Exact Match: False

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Initialize the first two Fibonacci numbers
fib_sequence = [0, 1]

# Print the first two Fibonacci numbers
print("Fibonacci sequence:", fib_sequence)

# Compute the Fibonacci sequence up to 100
for i in range(2, 100):
    fib_sequence.append(fibonacci(i))

# Print all Fibonacci numbers less than 100
print("Fibonacci numbers less than 100:", fib_sequence)