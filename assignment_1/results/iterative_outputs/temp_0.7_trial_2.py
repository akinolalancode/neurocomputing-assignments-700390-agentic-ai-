# Temperature: 0.7
# Top-p: 0.95
# Executable: True
# Correct: True
# Exact Match: True

def fibonacci_sequence(limit):
    fib_sequence = []
    a, b = 0, 1
    
    # Generate Fibonacci numbers until the next one exceeds the limit
    while a < limit:
        fib_sequence.append(a)
        a, b = b, a + b
    
    return fib_sequence

# Compute the Fibonacci sequence up to the 100th number
fibonacci_numbers = fibonacci_sequence(100)

# Print each Fibonacci number that is less than 100
for number in fibonacci_numbers:
    if number < 100:
        print(number)