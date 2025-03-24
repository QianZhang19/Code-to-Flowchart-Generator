#!/usr/bin/env python3
"""
Calculator Flowchart Generator
A script to create a flowchart for a simple calculator program.
"""

import os
import sys
import argparse
from rich.console import Console
from rich.panel import Panel

from generators.simple_flowchart_generator import SimpleFlowchartGenerator

console = Console()

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a calculator flowchart",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path",
        default="calculator_flowchart.png"
    )

    parser.add_argument(
        "-f", "--format",
        help="Output format (png, svg, pdf)",
        choices=["png", "svg", "pdf"],
        default="png"
    )

    parser.add_argument(
        "-c", "--color-scheme",
        help="Color scheme for the flowchart",
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
    """Main function to generate a calculator flowchart."""
    args = parse_arguments()

    try:
        console.print(
            Panel.fit(
                "[bold blue]Calculator Flowchart Generator[/bold blue]\n"
                "[italic]Creating a flowchart for a simple calculator program[/italic]",
                border_style="blue"
            )
        )

        # Create calculator flowchart structure with perfectly aligned grid layout
        flowchart = {
            "nodes": [
                {"id": 0, "type": "start_end", "text": "Start", "x": 0.5, "y": 0.95},
                {"id": 1, "type": "input_output", "text": "Input num1", "x": 0.5, "y": 0.85},
                {"id": 2, "type": "input_output", "text": "Input num2", "x": 0.5, "y": 0.75},
                {"id": 3, "type": "input_output", "text": "Input operation", "x": 0.5, "y": 0.65},
                {"id": 4, "type": "decision", "text": "operation == '+'", "x": 0.5, "y": 0.55},
                {"id": 5, "type": "process", "text": "result = num1 + num2", "x": 0.75, "y": 0.55},
                {"id": 6, "type": "decision", "text": "operation == '-'", "x": 0.5, "y": 0.45},
                {"id": 7, "type": "process", "text": "result = num1 - num2", "x": 0.75, "y": 0.45},
                {"id": 8, "type": "decision", "text": "operation == '*'", "x": 0.5, "y": 0.35},
                {"id": 9, "type": "process", "text": "result = num1 * num2", "x": 0.75, "y": 0.35},
                {"id": 10, "type": "decision", "text": "operation == '/'", "x": 0.5, "y": 0.25},
                {"id": 11, "type": "process", "text": "result = num1 / num2", "x": 0.75, "y": 0.25},
                {"id": 12, "type": "process", "text": "result = 'Invalid'", "x": 0.5, "y": 0.15},
                {"id": 13, "type": "input_output", "text": "Output result", "x": 0.5, "y": 0.05},
                {"id": 14, "type": "start_end", "text": "End", "x": 0.25, "y": 0.05}
            ],
            "edges": [
                {"from": 0, "to": 1, "text": ""},
                {"from": 1, "to": 2, "text": ""},
                {"from": 2, "to": 3, "text": ""},
                {"from": 3, "to": 4, "text": ""},
                {"from": 4, "to": 5, "text": "Yes"},
                {"from": 4, "to": 6, "text": "No"},
                {"from": 5, "to": 13, "text": ""},
                {"from": 6, "to": 7, "text": "Yes"},
                {"from": 6, "to": 8, "text": "No"},
                {"from": 7, "to": 13, "text": ""},
                {"from": 8, "to": 9, "text": "Yes"},
                {"from": 8, "to": 10, "text": "No"},
                {"from": 9, "to": 13, "text": ""},
                {"from": 10, "to": 11, "text": "Yes"},
                {"from": 10, "to": 12, "text": "No"},
                {"from": 11, "to": 13, "text": ""},
                {"from": 12, "to": 13, "text": ""},
                {"from": 13, "to": 14, "text": ""}
            ]
        }

        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate flowchart
        console.print(f"Generating {args.format.upper()} flowchart with [green]{args.color_scheme}[/green] color scheme...")
        generator = SimpleFlowchartGenerator(color_scheme=args.color_scheme)
        generator.generate_from_structure(flowchart, args.output, args.format)

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
