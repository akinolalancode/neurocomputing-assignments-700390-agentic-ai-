# Temperature: 0.7
# Top-p: 0.95
# Executable: True
# Correct: False
# Exact Match: False

def fibonacci(n):
    # Base case: the first two Fibonacci numbers are 0 and 1
    if n == 0 or n == 1:
        return n
    # Recursive case: sum of the two preceding Fibonacci numbers
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    # Initialize the first two Fibonacci numbers
    a, b = 0, 1
    
    # Print all Fibonacci numbers less than 100
    while a < 100:
        print(f"Fibonacci({a}) = {a}")
        # Move to the next Fibonacci number
        a, b = b, a + b

if __name__ == "__main__":
    main()