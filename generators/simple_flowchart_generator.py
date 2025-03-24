"""
Simple Flowchart generator for the Code to Flowchart tool.
Creates traditional flowcharts with standard shapes and connections.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict, List, Any, Tuple, Optional

class SimpleFlowchartGenerator:
    """Generator for creating simple, traditional flowcharts."""

    # Shape definitions
    SHAPES = {
        "start_end": "ellipse",
        "process": "rectangle",
        "decision": "diamond",
        "input_output": "parallelogram"
    }

    # Color schemes
    COLOR_SCHEMES = {
        "standard": {
            "background": "white",
            "start_end": "#4CAF50",  # Green
            "process": "#2196F3",    # Blue
            "decision": "#FFC107",   # Amber
            "input_output": "#FF9800", # Orange
            "connector": "#607D8B",  # Blue Grey
            "text": "black",
            "arrow": "black"
        },
        "pastel": {
            "background": "#F5F5F5",
            "start_end": "#A5D6A7",  # Light Green
            "process": "#90CAF9",    # Light Blue
            "decision": "#FFE082",   # Light Amber
            "input_output": "#FFCC80", # Light Orange
            "connector": "#B0BEC5",  # Light Blue Grey
            "text": "#37474F",       # Dark Blue Grey
            "arrow": "#455A64"       # Dark Blue Grey
        },
        "monochrome": {
            "background": "white",
            "start_end": "#212121",  # Very Dark Grey
            "process": "#424242",    # Dark Grey
            "decision": "#616161",   # Grey
            "input_output": "#757575", # Light Grey
            "connector": "#9E9E9E",  # Very Light Grey
            "text": "white",
            "arrow": "black"
        },
        "colorful": {
            "background": "white",
            "start_end": "#4CAF50",  # Green
            "process": "#2196F3",    # Blue
            "decision": "#FFC107",   # Amber
            "input_output": "#FF5722", # Deep Orange
            "connector": "#9C27B0",  # Purple
            "text": "black",
            "arrow": "#3F51B5"       # Indigo
        }
    }

    def __init__(self, color_scheme: str = "standard"):
        """
        Initialize the flowchart generator.

        Args:
            color_scheme: The color scheme to use (standard, pastel, monochrome, colorful)
        """
        self.colors = self.COLOR_SCHEMES.get(color_scheme, self.COLOR_SCHEMES["standard"])
        self.is_complex = False
        self.node_count = 0

    def generate_from_code(self, code: str, output_path: str, output_format: str = "png") -> None:
        """
        Generate a flowchart from code.

        Args:
            code: The source code to convert to a flowchart
            output_path: Path to save the generated flowchart
            output_format: Format of the output file (png, svg, pdf)
        """
        flowchart = self._parse_code(code)

        self.node_count = len(flowchart.get("nodes", []))
        self.is_complex = self._determine_complexity(flowchart)

        self._generate_flowchart(flowchart, output_path, output_format)

    def generate_from_structure(self, flowchart: Dict[str, Any], output_path: str, output_format: str = "png") -> None:
        """
        Generate a flowchart from a predefined structure.

        Args:
            flowchart: The flowchart structure
            output_path: Path to save the generated flowchart
            output_format: Format of the output file (png, svg, pdf)
        """
        self.node_count = len(flowchart.get("nodes", []))
        self.is_complex = self._determine_complexity(flowchart)

        self._generate_flowchart(flowchart, output_path, output_format)

    def _parse_code(self, code: str) -> Dict[str, Any]:
        """
        Parse code into a flowchart structure.
        This is a simplified parser for demonstration purposes.

        Args:
            code: The source code to parse

        Returns:
            A dictionary representing the flowchart structure
        """
        # This is a placeholder for a more sophisticated parser
        # In a real implementation, this would analyze the code and create a proper flowchart structure

        return {
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

    def _generate_flowchart(self, flowchart: Dict[str, Any], output_path: str, output_format: str = "png") -> None:
        """
        Generate a flowchart visualization.

        Args:
            flowchart: The flowchart structure
            output_path: Path to save the generated flowchart
            output_format: Format of the output file (png, svg, pdf)
        """
        fig, ax = plt.subplots(figsize=(10, 12), facecolor=self.colors["background"])

        ax.grid(False)

        # Draw nodes
        node_patches = {}
        node_centers = {}
        node_shapes = {}
        for node in flowchart["nodes"]:
            node_id = node["id"]
            node_type = node["type"]
            node_text = node["text"]
            x, y = node["x"], node["y"]

            node_centers[node_id] = (x, y)

            shape = self._create_shape(node_type, x, y)
            node_shapes[node_id] = shape

            color = self.colors.get(node_type, self.colors["process"])

            patch = self._add_shape_to_plot(ax, shape, color)
            node_patches[node_id] = (patch, x, y, node_type)

            self._add_text_to_shape(ax, node_type, x, y, node_text)

        for edge in flowchart["edges"]:
            from_id = edge["from"]
            to_id = edge["to"]
            edge_text = edge["text"]

            source = node_patches[from_id]
            target = node_patches[to_id]
            source_shape = node_shapes[from_id]
            target_shape = node_shapes[to_id]

            # Draw arrow
            self._draw_arrow(ax, source, target, source_shape, target_shape, edge_text)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Save the plot
        plt.tight_layout()

        if output_format == "svg":
            plt.savefig(output_path, format='svg', bbox_inches='tight', dpi=300)
        elif output_format == "pdf":
            plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
        else:
            plt.savefig(output_path, format='png', bbox_inches='tight', dpi=300)

        plt.close()

    def _create_shape(self, shape_type: str, x: float, y: float) -> Dict[str, Any]:
        """
        Create a shape definition based on the shape type.

        Args:
            shape_type: Type of shape to create
            x: X-coordinate of the shape center
            y: Y-coordinate of the shape center

        Returns:
            Dictionary with shape properties
        """
        # Adjust dimensions based on complexity
        if self.is_complex:
            width = 0.12
            height = 0.06
            diamond_size = 0.06
        else:
            # Normal sizes for simple flowcharts
            width = 0.16
            height = 0.08
            diamond_size = 0.08

        if shape_type == "start_end":
            return {
                "type": "ellipse",
                "x": x - width/2,
                "y": y - height/2,
                "width": width,
                "height": height
            }
        elif shape_type == "process":
            return {
                "type": "rectangle",
                "x": x - width/2,
                "y": y - height/2,
                "width": width,
                "height": height
            }
        elif shape_type == "decision":
            # Diamond is larger
            return {
                "type": "diamond",
                "x": x,
                "y": y,
                "size": diamond_size
            }
        elif shape_type == "input_output":
            # Parallelogram has a slight offset
            return {
                "type": "parallelogram",
                "x": x - width/2,
                "y": y - height/2,
                "width": width,
                "height": height,
                "offset": width/6
            }
        else:
            # Default to rectangle
            return {
                "type": "rectangle",
                "x": x - width/2,
                "y": y - height/2,
                "width": width,
                "height": height
            }

    def _add_shape_to_plot(self, ax: plt.Axes, shape: Dict[str, Any], color: str) -> patches.Patch:
        """
        Add a shape to the plot.

        Args:
            ax: Matplotlib axes
            shape: Shape definition
            color: Fill color for the shape

        Returns:
            The created patch
        """
        if shape["type"] == "ellipse":
            patch = patches.Ellipse(
                (shape["x"] + shape["width"]/2, shape["y"] + shape["height"]/2),
                shape["width"],
                shape["height"],
                facecolor=color,
                edgecolor='black',
                linewidth=1.5,
                alpha=0.9
            )
            ax.add_patch(patch)
            return patch

        elif shape["type"] == "rectangle":
            patch = patches.Rectangle(
                (shape["x"], shape["y"]),
                shape["width"],
                shape["height"],
                facecolor=color,
                edgecolor='black',
                linewidth=1.5,
                alpha=0.9
            )
            ax.add_patch(patch)
            return patch

        elif shape["type"] == "diamond":
            x, y = shape["x"], shape["y"]
            size = shape["size"]

            diamond_points = [
                [x, y + size],  # top
                [x + size, y],  # right
                [x, y - size],  # bottom
                [x - size, y]   # left
            ]

            patch = patches.Polygon(
                diamond_points,
                facecolor=color,
                edgecolor='black',
                linewidth=1.5,
                alpha=0.9
            )
            ax.add_patch(patch)
            return patch

        elif shape["type"] == "parallelogram":
            x, y = shape["x"], shape["y"]
            width, height = shape["width"], shape["height"]
            offset = shape["offset"]

            parallelogram_points = [
                [x + offset, y],  # bottom left
                [x + width + offset, y],  # bottom right
                [x + width, y + height],  # top right
                [x, y + height]  # top left
            ]

            patch = patches.Polygon(
                parallelogram_points,
                facecolor=color,
                edgecolor='black',
                linewidth=1.5,
                alpha=0.9
            )
            ax.add_patch(patch)
            return patch

        else:
            patch = patches.Rectangle(
                (shape["x"], shape["y"]),
                shape["width"],
                shape["height"],
                facecolor=color,
                edgecolor='black',
                linewidth=1.5,
                alpha=0.9
            )
            ax.add_patch(patch)
            return patch

    def _add_text_to_shape(self, ax: plt.Axes, shape_type: str, x: float, y: float, text: str) -> None:
        """
        Add text to a shape.

        Args:
            ax: Matplotlib axes
            shape_type: Type of shape
            x: X-coordinate of the shape center
            y: Y-coordinate of the shape center
            text: Text to add
        """
        font_size = 8 if self.is_complex else 10

        if shape_type == "decision":
            ax.text(x, y, text, ha='center', va='center', wrap=True,
                    fontsize=font_size, color=self.colors.get("text", "black"))
        else:
            ax.text(x, y, text, ha='center', va='center', wrap=True,
                    fontsize=font_size, color=self.colors.get("text", "black"))

    def _get_connection_points(self, source_type: str, target_type: str,
                              source_x: float, source_y: float,
                              target_x: float, target_y: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """
        Calculate the exact connection points between two shapes for straight lines.

        Args:
            source_type: Type of source shape
            target_type: Type of target shape
            source_x: X-coordinate of source shape center
            source_y: Y-coordinate of source shape center
            target_x: X-coordinate of target shape center
            target_y: Y-coordinate of target shape center

        Returns:
            Tuple of (start_point, end_point)
        """
        is_vertical = abs(target_y - source_y) > abs(target_x - source_x)

        if is_vertical and abs(target_x - source_x) < 0.05:
            if source_y > target_y:  # Going down
                if source_type == "start_end":
                    start_y = source_y - 0.04
                elif source_type == "process":
                    start_y = source_y - 0.04
                elif source_type == "decision":
                    start_y = source_y - 0.08
                elif source_type == "input_output":
                    start_y = source_y - 0.04
                else:
                    start_y = source_y - 0.04

                if target_type == "start_end":
                    end_y = target_y + 0.04
                elif target_type == "process":
                    end_y = target_y + 0.04
                elif target_type == "decision":
                    end_y = target_y + 0.08
                elif target_type == "input_output":
                    end_y = target_y + 0.04
                else:
                    end_y = target_y + 0.04
            else:  # Going up
                if source_type == "start_end":
                    start_y = source_y + 0.04
                elif source_type == "process":
                    start_y = source_y + 0.04
                elif source_type == "decision":
                    start_y = source_y + 0.08
                elif source_type == "input_output":
                    start_y = source_y + 0.04
                else:
                    start_y = source_y + 0.04

                if target_type == "start_end":
                    end_y = target_y - 0.04
                elif target_type == "process":
                    end_y = target_y - 0.04
                elif target_type == "decision":
                    end_y = target_y - 0.08
                elif target_type == "input_output":
                    end_y = target_y - 0.04
                else:
                    end_y = target_y - 0.04

            return (source_x, start_y), (target_x, end_y)

        elif not is_vertical and abs(target_y - source_y) < 0.05:
            if source_x > target_x:  # Going left
                if source_type == "start_end":
                    start_x = source_x - 0.08
                elif source_type == "process":
                    start_x = source_x - 0.08
                elif source_type == "decision":
                    start_x = source_x - 0.08
                elif source_type == "input_output":
                    start_x = source_x - 0.08
                else:
                    start_x = source_x - 0.08

                if target_type == "start_end":
                    end_x = target_x + 0.08
                elif target_type == "process":
                    end_x = target_x + 0.08
                elif target_type == "decision":
                    end_x = target_x + 0.08
                elif target_type == "input_output":
                    end_x = target_x + 0.08
                else:
                    end_x = target_x + 0.08
            else:  # Going right
                if source_type == "start_end":
                    start_x = source_x + 0.08
                elif source_type == "process":
                    start_x = source_x + 0.08
                elif source_type == "decision":
                    start_x = source_x + 0.08
                elif source_type == "input_output":
                    start_x = source_x + 0.08
                else:
                    start_x = source_x + 0.08

                if target_type == "start_end":
                    end_x = target_x - 0.08
                elif target_type == "process":
                    end_x = target_x - 0.08
                elif target_type == "decision":
                    end_x = target_x - 0.08
                elif target_type == "input_output":
                    end_x = target_x - 0.08
                else:
                    end_x = target_x - 0.08

            return (start_x, source_y), (end_x, target_y)

        elif source_x > 0.6 and target_x == 0.5 and source_y < target_y:
            return (source_x, source_y - 0.04), (target_x + 0.08, target_y)

        else:
            if source_type == "decision" and target_x > source_x:
                return (source_x + 0.08, source_y), (target_x - 0.08, target_y)
            elif source_type == "decision" and target_x < source_x:
                return (source_x - 0.08, source_y), (target_x + 0.08, target_y)
            else:
                return (source_x, source_y), (target_x, target_y)

    def _draw_arrow(self, ax: plt.Axes, source: Tuple[patches.Patch, float, float, str],
                   target: Tuple[patches.Patch, float, float, str],
                   source_shape: Dict[str, Any], target_shape: Dict[str, Any],
                   text: str) -> None:
        """
        Draw an arrow between two shapes.

        Args:
            ax: Matplotlib axes
            source: Source shape (patch, x, y, type)
            target: Target shape (patch, x, y, type)
            source_shape: Source shape definition
            target_shape: Target shape definition
            text: Text to add to the arrow
        """
        source_patch, source_x, source_y, source_type = source
        target_patch, target_x, target_y, target_type = target

        start_point, end_point = self._get_connection_points(
            source_type, target_type, source_x, source_y, target_x, target_y
        )

        arrow_color = self.colors.get("arrow", "black")

        if source_x > 0.6 and target_x == 0.5 and source_y < target_y:
            ax.plot(
                [start_point[0], start_point[0]],
                [start_point[1], start_point[1] - 0.05],
                color=arrow_color,
                linewidth=1.5
            )

            ax.plot(
                [start_point[0], target_x],
                [start_point[1] - 0.05, start_point[1] - 0.05],
                color=arrow_color,
                linewidth=1.5
            )

            ax.annotate(
                "",
                xy=(target_x, target_y - 0.08),
                xytext=(target_x, start_point[1] - 0.05),
                arrowprops=dict(
                    arrowstyle="->",
                    color=arrow_color,
                    linewidth=1.5,
                    connectionstyle="arc3,rad=0"
                )
            )

        elif source_type == "decision":
            if target_x > source_x:
                ax.annotate(
                    "",
                    xy=end_point,
                    xytext=start_point,
                    arrowprops=dict(
                        arrowstyle="->",
                        color=arrow_color,
                        linewidth=1.5,
                        connectionstyle="arc3,rad=0"
                    )
                )

                # Add Yes text
                if text:
                    mid_x = (start_point[0] + end_point[0]) / 2
                    mid_y = (start_point[1] + end_point[1]) / 2
                    ax.text(
                        mid_x, mid_y + 0.02,
                        text,
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=9,
                        fontweight='bold',
                        color='green',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
                    )
            # No branch (to the left)
            else:
                ax.annotate(
                    "",
                    xy=end_point,
                    xytext=start_point,
                    arrowprops=dict(
                        arrowstyle="->",
                        color=arrow_color,
                        linewidth=1.5,
                        connectionstyle="arc3,rad=0"
                    )
                )

                # Add No text
                if text:
                    mid_x = (start_point[0] + end_point[0]) / 2
                    mid_y = (start_point[1] + end_point[1]) / 2
                    ax.text(
                        mid_x, mid_y + 0.02,
                        text,
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=9,
                        fontweight='bold',
                        color='red',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
                    )

        # Default straight arrow for all other connections
        else:
            ax.annotate(
                "",
                xy=end_point,
                xytext=start_point,
                arrowprops=dict(
                    arrowstyle="->",
                    color=arrow_color,
                    linewidth=1.5,
                    connectionstyle="arc3,rad=0"
                )
            )

    def _determine_complexity(self, flowchart: Dict[str, Any]) -> bool:
        """
        Determine if the flowchart is complex based on various factors.

        Args:
            flowchart: The flowchart structure

        Returns:
            True if the flowchart is complex, False otherwise
        """
        nodes = flowchart.get("nodes", [])
        edges = flowchart.get("edges", [])

        # Consider a flowchart complex if it has more than 10 nodes
        if len(nodes) > 10:
            return True

        # Count decision nodes (more decisions = more complex)
        decision_count = sum(1 for node in nodes if node.get("type") == "decision")
        if decision_count > 3:
            return True

        # Count loops (edges that point to previous nodes)
        node_ids = {node["id"]: i for i, node in enumerate(nodes)}
        loops = 0
        for edge in edges:
            from_idx = node_ids.get(edge["from"], 0)
            to_idx = node_ids.get(edge["to"], 0)
            if to_idx < from_idx:  # Edge points backward
                loops += 1

        if loops > 1:
            return True

        return False
