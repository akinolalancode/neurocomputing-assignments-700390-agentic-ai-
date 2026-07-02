# Temperature: 0.3
# Top-p: 0.95
# Executable: True
# Correct: True
# Exact Match: True

def fibonacci_sequence():
    a, b = 0, 1
    while a < 100:
        print(a)
        a, b = b, a + b

# Call the function to compute the Fibonacci sequence
fibonacci_sequence()