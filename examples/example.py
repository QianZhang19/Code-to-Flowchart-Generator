#!/usr/bin/env python3
"""
Example Python file to demonstrate the code-to-flowchart tool.
This file contains various Python constructs that will be visualized in the flowchart.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional


def calculate_factorial(n: int) -> int:
    """
    Calculate the factorial of a number recursively.
    
    Args:
        n: The number to calculate factorial for
        
    Returns:
        The factorial of n
    """
    if n <= 1:
        return 1
    else:
        return n * calculate_factorial(n - 1)


def find_max_min(numbers: List[int]) -> Dict[str, int]:
    """
    Find the maximum and minimum values in a list of numbers.
    
    Args:
        numbers: List of numbers to analyze
        
    Returns:
        Dictionary containing the max and min values
    """
    if not numbers:
        return {"max": None, "min": None}
    
    max_value = numbers[0]
    min_value = numbers[0]
    
    for num in numbers:
        if num > max_value:
            max_value = num
        if num < min_value:
            min_value = num
    
    return {"max": max_value, "min": min_value}


class DataProcessor:
    """A class to process and analyze data."""
    
    def __init__(self, data: List[Any]):
        """
        Initialize the DataProcessor with data.
        
        Args:
            data: The data to process
        """
        self.data = data
        self.processed = False
    
    def process_data(self) -> None:
        """Process the data."""
        if not self.data:
            print("No data to process")
            return
        
        try:
            # Simulate data processing
            print(f"Processing {len(self.data)} items...")
            
            for i, item in enumerate(self.data):
                # Do something with each item
                print(f"Processing item {i}: {item}")
            
            self.processed = True
            print("Data processing complete")
            
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            self.processed = False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculate statistics on the processed data.
        
        Returns:
            Dictionary of statistics
        """
        if not self.processed:
            print("Data has not been processed yet")
            return {}
        
        numeric_data = []
        for item in self.data:
            if isinstance(item, (int, float)):
                numeric_data.append(item)
        
        if not numeric_data:
            return {"count": len(self.data), "numeric_count": 0}
        
        stats = {
            "count": len(self.data),
            "numeric_count": len(numeric_data),
            "sum": sum(numeric_data),
            "average": sum(numeric_data) / len(numeric_data)
        }
        
        # Add min and max if there are numeric values
        if numeric_data:
            result = find_max_min(numeric_data)
            stats.update(result)
        
        return stats


def main() -> int:
    """Main function to demonstrate various Python constructs."""
    # Example of variable assignment
    sample_data = [1, 5, 10, 15, 20, "hello", "world"]
    
    # Example of conditional statement
    if len(sample_data) > 5:
        print(f"Sample data has {len(sample_data)} items")
    else:
        print("Sample data has 5 or fewer items")
    
    # Example of function call
    factorial_5 = calculate_factorial(5)
    print(f"Factorial of 5 is {factorial_5}")
    
    # Example of class instantiation and method calls
    processor = DataProcessor(sample_data)
    processor.process_data()
    
    # Example of try-except block
    try:
        stats = processor.get_statistics()
        print("Statistics:", json.dumps(stats, indent=2))
        
        # Example of file operations
        with open("stats.json", "w") as f:
            json.dump(stats, f, indent=2)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
