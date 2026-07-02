# Temperature: 0.0
# Top-p: 0.95
# Executable: True
# Correct: False
# Exact Match: False

def fibonacci_sequence(limit):
    fib_sequence = []
    a, b = 0, 1
    
    while a < limit:
        fib_sequence.append(a)
        a, b = b, a + b
    
    return fib_sequence

# Set the limit to 100
limit = 100

# Get the Fibonacci sequence
fibonacci_numbers = fibonacci_sequence(limit)

# Print each Fibonacci number less than 100
print("Fibonacci sequence less than 100:")
for number in fibonacci_numbers:
    print(number)