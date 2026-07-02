# Temperature: 0.5
# Top-p: 0.95
# Executable: True
# Correct: True
# Exact Match: True

def fibonacci_sequence():
    # Initialize the first two Fibonacci numbers
    a, b = 0, 1
    
    # Loop until a Fibonacci number is less than 100
    while a < 100:
        print(a)
        
        # Update the next Fibonacci number
        a, b = b, a + b

# Call the function to compute and print the Fibonacci sequence
fibonacci_sequence()