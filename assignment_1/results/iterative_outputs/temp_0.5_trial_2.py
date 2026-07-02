# Temperature: 0.5
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

# Get all Fibonacci numbers less than 100
fib_numbers = fibonacci_sequence()

# Print each Fibonacci number
print("Fibonacci sequence less than 100:")
for num in fib_numbers:
    print(num)