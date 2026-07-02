# Temperature: 0.7
# Top-p: 0.95
# Executable: True
# Correct: True
# Exact Match: True

def fibonacci_sequence():
    # Initialize the first two Fibonacci numbers
    a, b = 0, 1
    
    # Loop until the next Fibonacci number is less than 100
    while a < 100:
        # Print the current Fibonacci number
        print(a)
        
        # Update the next Fibonacci number
        a, b = b, a + b

# Call the function to compute the Fibonacci sequence
fibonacci_sequence()