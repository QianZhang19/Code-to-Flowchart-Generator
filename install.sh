#!/bin/bash
# Installation script for the code-to-flowchart tool

echo "Installing code-to-flowchart tool..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r "$SCRIPT_DIR/requirements.txt"

# Check if Graphviz is installed
if ! command -v dot &> /dev/null; then
    echo "Graphviz not found. Please install Graphviz:"
    echo "  macOS: brew install graphviz"
    echo "  Ubuntu/Debian: sudo apt-get install graphviz"
    echo "  Windows: Download from https://graphviz.org/download/"
    exit 1
fi

echo "Installation complete!"
echo "You can now use the tool by running: $SCRIPT_DIR/co_to_f <python_file>"
