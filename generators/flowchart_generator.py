# """
# Flowchart generator for the Code to Flowchart tool.
# Converts parsed code structure into visual flowcharts.
# """

# import os
# import networkx as nx
# import matplotlib.pyplot as plt
# from typing import Dict, List, Any, Optional, Tuple


# class FlowchartGenerator:
#     """Generator for creating flowcharts from parsed code structures."""

#     # Theme definitions
#     THEMES = {
#         "default": {
#             "background_color": "white",
#             "node_colors": {
#                 "module": "#E0F7FA",
#                 "function": "#B3E5FC",
#                 "class": "#BBDEFB",
#                 "if": "#C8E6C9",
#                 "for": "#DCEDC8",
#                 "while": "#F0F4C3",
#                 "try": "#FFF9C4",
#                 "except": "#FFECB3",
#                 "return": "#FFCCBC",
#                 "assign": "#D7CCC8",
#                 "expr": "#F5F5F5",
#                 "import": "#E1BEE7",
#                 "import_from": "#D1C4E9",
#                 "default": "#EEEEEE"
#             },
#             "edge_colors": {
#                 "normal": "black",
#                 "true": "green",
#                 "false": "red",
#                 "exception": "orange",
#                 "default": "gray"
#             },
#             "font_name": "Arial",
#             "font_size": 10,
#             "node_shape": "box",
#             "edge_style": "solid"
#         },
#         "dark": {
#             "background_color": "#2D2D2D",
#             "node_colors": {
#                 "module": "#263238",
#                 "function": "#1A237E",
#                 "class": "#0D47A1",
#                 "if": "#1B5E20",
#                 "for": "#33691E",
#                 "while": "#F57F17",
#                 "try": "#FF6F00",
#                 "except": "#E65100",
#                 "return": "#BF360C",
#                 "assign": "#3E2723",
#                 "expr": "#212121",
#                 "import": "#4A148C",
#                 "import_from": "#311B92",
#                 "default": "#424242"
#             },
#             "edge_colors": {
#                 "normal": "white",
#                 "true": "#00C853",
#                 "false": "#FF5252",
#                 "exception": "#FFAB40",
#                 "default": "#BDBDBD"
#             },
#             "font_name": "Arial",
#             "font_size": 10,
#             "font_color": "white",
#             "node_shape": "box",
#             "edge_style": "solid"
#         },
#         "light": {
#             "background_color": "#FAFAFA",
#             "node_colors": {
#                 "module": "#ECEFF1",
#                 "function": "#E3F2FD",
#                 "class": "#E8EAF6",
#                 "if": "#E8F5E9",
#                 "for": "#F1F8E9",
#                 "while": "#FFFDE7",
#                 "try": "#FFF8E1",
#                 "except": "#FFF3E0",
#                 "return": "#FBE9E7",
#                 "assign": "#EFEBE9",
#                 "expr": "#FAFAFA",
#                 "import": "#F3E5F5",
#                 "import_from": "#EDE7F6",
#                 "default": "#F5F5F5"
#             },
#             "edge_colors": {
#                 "normal": "#424242",
#                 "true": "#2E7D32",
#                 "false": "#C62828",
#                 "exception": "#EF6C00",
#                 "default": "#9E9E9E"
#             },
#             "font_name": "Arial",
#             "font_size": 10,
#             "node_shape": "box",
#             "edge_style": "solid"
#         },
#         "colorful": {
#             "background_color": "white",
#             "node_colors": {
#                 "module": "#E1F5FE",
#                 "function": "#B39DDB",
#                 "class": "#90CAF9",
#                 "if": "#80CBC4",
#                 "for": "#A5D6A7",
#                 "while": "#FFF59D",
#                 "try": "#FFE082",
#                 "except": "#FFAB91",
#                 "return": "#EF9A9A",
#                 "assign": "#CE93D8",
#                 "expr": "#80DEEA",
#                 "import": "#9FA8DA",
#                 "import_from": "#81D4FA",
#                 "default": "#B0BEC5"
#             },
#             "edge_colors": {
#                 "normal": "#5D4037",
#                 "true": "#00897B",
#                 "false": "#D32F2F",
#                 "exception": "#FF7043",
#                 "default": "#616161"
#             },
#             "font_name": "Arial",
#             "font_size": 10,
#             "node_shape": "box",
#             "edge_style": "solid"
#         }
#     }

#     def __init__(self, theme: str = "default"):
#         """
#         Initialize the flowchart generator.

#         Args:
#             theme: The theme to use for the flowchart
#         """
#         self.theme = self.THEMES.get(theme, self.THEMES["default"])

#     def generate(self, parsed_code: Dict[str, Any], output_path: str, output_format: str = "png") -> None:
#         """
#         Generate a flowchart from parsed code.

#         Args:
#             parsed_code: The parsed code structure
#             output_path: Path to save the generated flowchart
#             output_format: Format of the output file (png, svg, pdf)
#         """
#         G = nx.DiGraph()

#         node_labels = {}
#         node_colors = []
#         node_sizes = []

#         for node in parsed_code["nodes"]:
#             node_id = node["id"]
#             node_type = node["type"]
#             node_label = node["label"]

#             G.add_node(node_id)
#             node_labels[node_id] = node_label

#             fill_color = self.theme["node_colors"].get(
#                 node_type,
#                 self.theme["node_colors"]["default"]
#             )
#             node_colors.append(fill_color)

#             size = 1000 + len(node_label) * 20
#             node_sizes.append(min(size, 3000))

#         # Add edges to the graph
#         edge_colors = []
#         edge_labels = {}

#         for edge in parsed_code["edges"]:
#             from_id = edge["from"]
#             to_id = edge["to"]
#             edge_type = edge["type"]

#             G.add_edge(from_id, to_id)

#             # Get edge color based on type
#             color = self.theme["edge_colors"].get(
#                 edge_type,
#                 self.theme["edge_colors"]["default"]
#             )
#             edge_colors.append(color)

#             # Add label for conditional edges
#             if edge_type == "true":
#                 edge_labels[(from_id, to_id)] = "True"
#             elif edge_type == "false":
#                 edge_labels[(from_id, to_id)] = "False"
#             elif edge_type == "exception":
#                 edge_labels[(from_id, to_id)] = "Exception"

#         node_count = len(parsed_code["nodes"])
#         fig_width = max(12, min(node_count / 2, 24))
#         fig_height = max(8, min(node_count / 3, 18))

#         plt.figure(figsize=(fig_width, fig_height), facecolor=self.theme["background_color"])

#         if node_count < 20:
#             pos = nx.spring_layout(G, seed=42, k=0.3)
#         elif node_count < 50:
#             try:
#                 pos = nx.kamada_kawai_layout(G)
#             except:
#                 pos = nx.spring_layout(G, seed=42)
#         else:
#             pos = nx.spring_layout(G, seed=42)

#         font_color = self.theme.get("font_color", "black")
#         nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9,
#                               edgecolors='black', linewidths=1)

#         for i, (u, v) in enumerate(G.edges()):
#             nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=1.5, alpha=0.8,
#                                   edge_color=edge_colors[i], arrows=True, arrowsize=15,
#                                   connectionstyle='arc3,rad=0.1')

#         font_size = self.theme["font_size"]
#         nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=font_size,
#                                font_color=font_color, font_family=self.theme["font_name"],
#                                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=4))

#         if edge_labels:
#             nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=font_size-2,
#                                         font_color=font_color, font_family=self.theme["font_name"])

#         plt.axis('off')
#         plt.tight_layout()

#         os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

#         if output_format == "svg":
#             plt.savefig(output_path, format='svg', bbox_inches='tight', dpi=300)
#         elif output_format == "pdf":
#             plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
#         else:
#             plt.savefig(output_path, format='png', bbox_inches='tight', dpi=300)

#         plt.close()
