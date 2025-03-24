#!/usr/bin/env python3
"""
Simple Flowchart Generator
A script to create traditional flowcharts with standard shapes and connections.
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
        description="Generate a simple flowchart",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path",
        default="flowchart.png"
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
    """Main function to generate a simple flowchart."""
    args = parse_arguments()

    try:
        # Print welcome message
        console.print(
            Panel.fit(
                "[bold blue]Simple Flowchart Generator[/bold blue]\n"
                "[italic]Creating traditional flowcharts with standard shapes[/italic]",
                border_style="blue"
            )
        )

        flowchart = {
            "nodes": [
                {"id": 0, "type": "start_end", "text": "Start", "x": 0.5, "y": 0.95},
                {"id": 1, "type": "input_output", "text": "Input a", "x": 0.5, "y": 0.80},
                {"id": 2, "type": "process", "text": "c = 1", "x": 0.5, "y": 0.65},
                {"id": 3, "type": "decision", "text": "c < 5", "x": 0.5, "y": 0.50},
                {"id": 4, "type": "process", "text": "Print a", "x": 0.7, "y": 0.50},
                {"id": 5, "type": "process", "text": "c = c + 1", "x": 0.7, "y": 0.35},
                {"id": 6, "type": "start_end", "text": "Stop", "x": 0.3, "y": 0.50}
            ],
            "edges": [
                {"from": 0, "to": 1, "text": ""},
                {"from": 1, "to": 2, "text": ""},
                {"from": 2, "to": 3, "text": ""},
                {"from": 3, "to": 4, "text": "Yes"},
                {"from": 3, "to": 6, "text": "No"},
                {"from": 4, "to": 5, "text": ""},
                {"from": 5, "to": 3, "text": ""}
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
