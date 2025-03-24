"""
File utility functions for the Code to Flowchart tool.
"""

import os
from typing import Optional


def read_file(file_path: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        The contents of the file as a string
        
    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there is an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()


def write_file(file_path: str, content: str) -> None:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        
    Raises:
        IOError: If there is an error writing to the file
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def ensure_dir_exists(directory_path: Optional[str]) -> None:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory to ensure exists
    """
    if directory_path and not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_file_extension(file_path: str) -> str:
    """
    Get the extension of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        The extension of the file (without the dot)
    """
    _, extension = os.path.splitext(file_path)
    return extension[1:] if extension else ""


def is_python_file(file_path: str) -> bool:
    """
    Check if a file is a Python file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a Python file, False otherwise
    """
    return get_file_extension(file_path).lower() == "py"
