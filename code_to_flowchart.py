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
from generators.flowchart_generator import FlowchartGenerator
from utils.file_utils import read_file, ensure_dir_exists

console = Console()

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
        help="Flowchart theme",
        choices=["default", "dark", "light", "colorful"],
        default="default"
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

        # Generate flowchart
        console.print(f"Generating {args.format.upper()} flowchart with [green]{args.theme}[/green] theme...")
        generator = FlowchartGenerator(theme=args.theme)
        generator.generate(parsed_code, args.output, args.format)

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
