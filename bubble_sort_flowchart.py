#!/usr/bin/env python3
"""
Bubble Sort Flowchart Generator
A script to create a flowchart for the bubble sort algorithm.
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
        description="Generate a bubble sort flowchart",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path",
        default="bubble_sort_flowchart.png"
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
    """Main function to generate a bubble sort flowchart."""
    args = parse_arguments()

    try:
        console.print(
            Panel.fit(
                "[bold blue]Bubble Sort Flowchart Generator[/bold blue]\n"
                "[italic]Creating a flowchart for the bubble sort algorithm[/italic]",
                border_style="blue"
            )
        )

        flowchart = {
            "nodes": [
                {"id": 0, "type": "start_end", "text": "Start", "x": 0.5, "y": 0.95},
                {"id": 1, "type": "input_output", "text": "Input array", "x": 0.5, "y": 0.87},
                {"id": 2, "type": "process", "text": "n = length(array)", "x": 0.5, "y": 0.79},
                {"id": 3, "type": "process", "text": "i = 0", "x": 0.5, "y": 0.71},
                {"id": 4, "type": "decision", "text": "i < n-1", "x": 0.5, "y": 0.63},
                {"id": 5, "type": "process", "text": "j = 0", "x": 0.5, "y": 0.55},
                {"id": 6, "type": "decision", "text": "j < n-i-1", "x": 0.5, "y": 0.47},
                {"id": 7, "type": "decision", "text": "array[j] > array[j+1]", "x": 0.5, "y": 0.39},
                {"id": 8, "type": "process", "text": "Swap array[j] and array[j+1]", "x": 0.75, "y": 0.39},
                {"id": 9, "type": "process", "text": "j = j + 1", "x": 0.5, "y": 0.31},
                {"id": 10, "type": "process", "text": "i = i + 1", "x": 0.5, "y": 0.23},
                {"id": 11, "type": "input_output", "text": "Output sorted array", "x": 0.5, "y": 0.15},
                {"id": 12, "type": "start_end", "text": "End", "x": 0.5, "y": 0.07}
            ],
            "edges": [
                {"from": 0, "to": 1, "text": ""},
                {"from": 1, "to": 2, "text": ""},
                {"from": 2, "to": 3, "text": ""},
                {"from": 3, "to": 4, "text": ""},
                {"from": 4, "to": 5, "text": "Yes"},
                {"from": 4, "to": 11, "text": "No"},
                {"from": 5, "to": 6, "text": ""},
                {"from": 6, "to": 7, "text": "Yes"},
                {"from": 6, "to": 10, "text": "No"},
                {"from": 7, "to": 8, "text": "Yes"},
                {"from": 7, "to": 9, "text": "No"},
                {"from": 8, "to": 9, "text": ""},
                {"from": 9, "to": 6, "text": ""},
                {"from": 10, "to": 4, "text": ""},
                {"from": 11, "to": 12, "text": ""}
            ]
        }

        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        console.print(f"Generating {args.format.upper()} flowchart with [green]{args.color_scheme}[/green] color scheme...")
        generator = SimpleFlowchartGenerator(color_scheme=args.color_scheme)
        generator.generate_from_structure(flowchart, args.output, args.format)

        console.print(f"[bold green]Success![/bold green] Flowchart saved to: [cyan]{args.output}[/cyan]")

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
