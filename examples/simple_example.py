#!/usr/bin/env python3
"""
Simple example for flowchart generation.
"""

def calculate_sum(n):
    """Calculate the sum of numbers from 1 to n."""
    total = 0
    i = 1
    
    while i <= n:
        total += i
        i += 1
    
    return total

def main():
    # Get user input
    number = int(input("Enter a number: "))
    
    # Calculate the sum
    result = calculate_sum(number)
    
    # Display the result
    print(f"The sum of numbers from 1 to {number} is: {result}")

if __name__ == "__main__":
    main()
