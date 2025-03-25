#!/usr/bin/env python3
"""
Code to Flowchart (co_to_f)
A tool to convert Python code into visual flowcharts.
"""

import os
import sys
import ast
import argparse
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

from parsers.python_parser import PythonParser
from generators.simple_flowchart_generator import SimpleFlowchartGenerator
from utils.file_utils import read_file, ensure_dir_exists

console = Console()

def adapt_parsed_code_for_simple_flowchart(parsed_code):
    """
    Adapt the output from PythonParser to be compatible with SimpleFlowchartGenerator.
    
    Args:
        parsed_code: The parsed code structure from PythonParser
        
    Returns:
        A dictionary with the structure expected by SimpleFlowchartGenerator
    """
    adapted_nodes = []
    adapted_edges = []
    
    # Calculate node positions
    node_count = len(parsed_code["nodes"])
    
    # Simple layout algorithm - place nodes in a grid
    cols = max(1, min(5, node_count // 5 + 1))  # Up to 5 columns
    row_height = 0.8 / (node_count // cols + 1)
    
    for i, node in enumerate(parsed_code["nodes"]):
        col = i % cols
        row = i // cols
        
        x = 0.1 + (col * (0.8 / cols))
        y = 0.9 - (row * row_height)
        
        # Convert label to text and add coordinates
        adapted_nodes.append({
            "id": node["id"],
            "type": map_node_type(node["type"]),
            "text": node["label"],
            "x": x,
            "y": y
        })
    
    # Convert edges
    for edge in parsed_code["edges"]:
        adapted_edges.append({
            "from": edge["from"],
            "to": edge["to"],
            "text": edge["type"] if edge["type"] in ["true", "false"] else ""
        })
    
    return {
        "nodes": adapted_nodes,
        "edges": adapted_edges
    }

def map_node_type(parser_type):
    """
    Map PythonParser node types to SimpleFlowchartGenerator node types.
    
    Args:
        parser_type: Node type from PythonParser
        
    Returns:
        Corresponding node type for SimpleFlowchartGenerator
    """
    type_mapping = {
        "module": "start_end",
        "function": "process",
        "class": "process",
        "if": "decision",
        "for": "process",
        "while": "process",
        "try": "process",
        "except": "process",
        "return": "process",
        "assign": "process",
        "expr": "process",
        "import": "process",
        "import_from": "process",
        "if_body": "process",
        "else_body": "process",
        "try_body": "process",
        "except_body": "process"
    }
    
    return type_mapping.get(parser_type, "process")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert code to flowchart",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "source_file",
        help="Path to the source code file"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: source_file_name.png)",
        default=None
    )

    parser.add_argument(
        "-f", "--format",
        help="Output format (png, svg, pdf)",
        choices=["png", "svg", "pdf"],
        default="png"
    )

    parser.add_argument(
        "-t", "--theme",
        help="Flowchart color scheme",
        choices=["standard", "pastel", "monochrome", "colorful"],
        default="standard"
    )

    parser.add_argument(
        "--show",
        help="Display the flowchart after generation",
        action="store_true"
    )

    return parser.parse_args()

def main():
    """Main function to convert code to flowchart."""
    args = parse_arguments()

    try:
        console.print(
            Panel.fit(
                "[bold blue]Code to Flowchart[/bold blue]\n"
                "[italic]Converting your code to visual flowcharts[/italic]",
                border_style="blue"
            )
        )

        if not os.path.exists(args.source_file):
            console.print(f"[bold red]Error:[/bold red] Source file '{args.source_file}' not found", style="red")
            return 1

        # Determine output file path
        if args.output is None:
            base_name = os.path.splitext(os.path.basename(args.source_file))[0]
            output_dir = os.path.dirname(args.source_file)
            args.output = os.path.join(output_dir, f"{base_name}_flowchart.{args.format}")

        # Ensure output directory exists
        ensure_dir_exists(os.path.dirname(args.output))

        # Read source code
        console.print(f"Reading source file: [cyan]{args.source_file}[/cyan]")
        source_code = read_file(args.source_file)

        # Parse the code
        console.print("Parsing code...")
        parser = PythonParser()
        parsed_code = parser.parse(source_code)
        
        # Adapt the parsed code for SimpleFlowchartGenerator
        adapted_code = adapt_parsed_code_for_simple_flowchart(parsed_code)

        # Generate flowchart
        console.print(f"Generating {args.format.upper()} flowchart with [green]{args.theme}[/green] color scheme...")
        generator = SimpleFlowchartGenerator(color_scheme=args.theme)
        generator.generate_from_structure(adapted_code, args.output, args.format)

        console.print(f"[bold green]Success![/bold green] Flowchart saved to: [cyan]{args.output}[/cyan]")

        # Show the flowchart if requested
        if args.show:
            console.print("Opening flowchart...")
            if sys.platform == "darwin":  # macOS
                os.system(f"open {args.output}")
            elif sys.platform == "win32":  # Windows
                os.system(f"start {args.output}")
            else:  # Linux
                os.system(f"xdg-open {args.output}")

        return 0

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        return 1

if __name__ == "__main__":
    sys.exit(main())
