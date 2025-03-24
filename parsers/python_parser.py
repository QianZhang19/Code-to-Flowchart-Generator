"""
Python code parser for the Code to Flowchart tool.
Parses Python code into a structured format suitable for flowchart generation.
"""

import ast
import json
from typing import Dict, List, Any, Union, Optional


class PythonParser:
    """Parser for Python code that converts it to a structured representation."""

    def __init__(self):
        self.node_counter = 0
        self.nodes = []
        self.edges = []
        self.current_parent = None

    def parse(self, source_code: str) -> Dict[str, Any]:
        """
        Parse Python source code into a structured representation.

        Args:
            source_code: The Python source code as a string

        Returns:
            A dictionary containing the parsed code structure
        """
        self.node_counter = 0
        self.nodes = []
        self.edges = []
        self.current_parent = None

        try:
            tree = ast.parse(source_code)
            self._process_node(tree)

            return {
                "nodes": self.nodes,
                "edges": self.edges
            }
        except SyntaxError as e:
            raise ValueError(f"Syntax error in Python code: {str(e)}")

    def _process_node(self, node: ast.AST, parent_id: Optional[int] = None) -> int:
        """
        Process an AST node and its children.

        Args:
            node: The AST node to process
            parent_id: ID of the parent node, if any

        Returns:
            The ID of the processed node
        """
        node_id = self.node_counter
        self.node_counter += 1

        # Save the previous parent
        prev_parent = self.current_parent
        self.current_parent = node_id

        # Connect to parent if exists
        if parent_id is not None:
            self.edges.append({
                "from": parent_id,
                "to": node_id,
                "type": "normal"
            })

        # Process different node types
        if isinstance(node, ast.Module):
            self.nodes.append({
                "id": node_id,
                "type": "module",
                "label": "Module"
            })
            for child in node.body:
                self._process_node(child, node_id)

        elif isinstance(node, ast.FunctionDef):
            args_str = ", ".join([arg.arg for arg in node.args.args])
            self.nodes.append({
                "id": node_id,
                "type": "function",
                "label": f"Function: {node.name}({args_str})"
            })
            for child in node.body:
                self._process_node(child, node_id)

        elif isinstance(node, ast.ClassDef):
            bases = [self._get_name(base) for base in node.bases]
            base_str = f"({', '.join(bases)})" if bases else ""
            self.nodes.append({
                "id": node_id,
                "type": "class",
                "label": f"Class: {node.name}{base_str}"
            })
            for child in node.body:
                self._process_node(child, node_id)

        elif isinstance(node, ast.If):
            test_str = self._expr_to_str(node.test)
            self.nodes.append({
                "id": node_id,
                "type": "if",
                "label": f"If: {test_str}"
            })

            # Process the 'if' body
            if_body_id = self.node_counter
            self.node_counter += 1
            self.nodes.append({
                "id": if_body_id,
                "type": "if_body",
                "label": "If body"
            })
            self.edges.append({
                "from": node_id,
                "to": if_body_id,
                "type": "true"
            })

            for child in node.body:
                self._process_node(child, if_body_id)

            # Process the 'else' body if it exists
            if node.orelse:
                else_body_id = self.node_counter
                self.node_counter += 1
                self.nodes.append({
                    "id": else_body_id,
                    "type": "else_body",
                    "label": "Else body"
                })
                self.edges.append({
                    "from": node_id,
                    "to": else_body_id,
                    "type": "false"
                })

                for child in node.orelse:
                    self._process_node(child, else_body_id)

        elif isinstance(node, ast.For):
            target_str = self._expr_to_str(node.target)
            iter_str = self._expr_to_str(node.iter)
            self.nodes.append({
                "id": node_id,
                "type": "for",
                "label": f"For: {target_str} in {iter_str}"
            })

            # Process loop body
            for child in node.body:
                self._process_node(child, node_id)

        elif isinstance(node, ast.While):
            test_str = self._expr_to_str(node.test)
            self.nodes.append({
                "id": node_id,
                "type": "while",
                "label": f"While: {test_str}"
            })

            # Process loop body
            for child in node.body:
                self._process_node(child, node_id)

        elif isinstance(node, ast.Try):
            self.nodes.append({
                "id": node_id,
                "type": "try",
                "label": "Try"
            })

            # Process try body
            try_body_id = self.node_counter
            self.node_counter += 1
            self.nodes.append({
                "id": try_body_id,
                "type": "try_body",
                "label": "Try body"
            })
            self.edges.append({
                "from": node_id,
                "to": try_body_id,
                "type": "normal"
            })

            for child in node.body:
                self._process_node(child, try_body_id)

            # Process except handlers
            for handler in node.handlers:
                except_id = self.node_counter
                self.node_counter += 1

                if handler.type:
                    exc_type = self._get_name(handler.type)
                    exc_name = handler.name if handler.name else ""
                    label = f"Except: {exc_type}" + (f" as {exc_name}" if exc_name else "")
                else:
                    label = "Except"

                self.nodes.append({
                    "id": except_id,
                    "type": "except",
                    "label": label
                })
                self.edges.append({
                    "from": node_id,
                    "to": except_id,
                    "type": "exception"
                })

                for child in handler.body:
                    self._process_node(child, except_id)

        elif isinstance(node, ast.Return):
            value_str = self._expr_to_str(node.value) if node.value else "None"
            self.nodes.append({
                "id": node_id,
                "type": "return",
                "label": f"Return: {value_str}"
            })

        elif isinstance(node, ast.Assign):
            targets_str = ", ".join([self._expr_to_str(target) for target in node.targets])
            value_str = self._expr_to_str(node.value)
            self.nodes.append({
                "id": node_id,
                "type": "assign",
                "label": f"{targets_str} = {value_str}"
            })

        elif isinstance(node, ast.Expr):
            expr_str = self._expr_to_str(node.value)
            self.nodes.append({
                "id": node_id,
                "type": "expr",
                "label": expr_str
            })

        elif isinstance(node, ast.Import):
            names = [name.name + (" as " + name.asname if name.asname else "") for name in node.names]
            self.nodes.append({
                "id": node_id,
                "type": "import",
                "label": f"Import: {', '.join(names)}"
            })

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = [name.name + (" as " + name.asname if name.asname else "") for name in node.names]
            self.nodes.append({
                "id": node_id,
                "type": "import_from",
                "label": f"From {module} import {', '.join(names)}"
            })

        else:
            # Generic handling for other node types
            self.nodes.append({
                "id": node_id,
                "type": node.__class__.__name__.lower(),
                "label": node.__class__.__name__
            })

        # Restore the previous parent
        self.current_parent = prev_parent

        return node_id

    def _expr_to_str(self, expr: Optional[ast.AST]) -> str:
        """
        Convert an expression AST node to a string representation.

        Args:
            expr: The expression AST node

        Returns:
            String representation of the expression
        """
        if expr is None:
            return "None"

        if isinstance(expr, ast.Name):
            return expr.id

        elif isinstance(expr, ast.Constant):
            if isinstance(expr.value, str):
                # Truncate long strings
                if len(expr.value) > 20:
                    return f'"{expr.value[:17]}..."'
                return f'"{expr.value}"'
            return str(expr.value)

        elif isinstance(expr, ast.Call):
            func_name = self._expr_to_str(expr.func)
            args = [self._expr_to_str(arg) for arg in expr.args]
            keywords = [f"{kw.arg}={self._expr_to_str(kw.value)}" for kw in expr.keywords]
            all_args = args + keywords

            # Truncate long argument lists
            if len(all_args) > 3:
                return f"{func_name}({', '.join(all_args[:2])}, ...)"
            return f"{func_name}({', '.join(all_args)})"

        elif isinstance(expr, ast.Attribute):
            return f"{self._expr_to_str(expr.value)}.{expr.attr}"

        elif isinstance(expr, ast.BinOp):
            left = self._expr_to_str(expr.left)
            right = self._expr_to_str(expr.right)
            op = self._get_op_symbol(expr.op)
            return f"{left} {op} {right}"

        elif isinstance(expr, ast.Compare):
            left = self._expr_to_str(expr.left)
            ops = [self._get_op_symbol(op) for op in expr.ops]
            comparators = [self._expr_to_str(comp) for comp in expr.comparators]

            result = left
            for i in range(len(ops)):
                result += f" {ops[i]} {comparators[i]}"
            return result

        elif isinstance(expr, ast.List):
            elts = [self._expr_to_str(elt) for elt in expr.elts]
            if len(elts) > 3:
                return f"[{', '.join(elts[:2])}, ...]"
            return f"[{', '.join(elts)}]"

        elif isinstance(expr, ast.Dict):
            if not expr.keys:
                return "{}"

            items = []
            for i in range(min(len(expr.keys), 3)):
                if expr.keys[i] is None:  # Handle **kwargs
                    items.append(f"**{self._expr_to_str(expr.values[i])}")
                else:
                    items.append(f"{self._expr_to_str(expr.keys[i])}: {self._expr_to_str(expr.values[i])}")

            if len(expr.keys) > 3:
                return f"{{{', '.join(items)}, ...}}"
            return f"{{{', '.join(items)}}}"

        return expr.__class__.__name__

    def _get_op_symbol(self, op: ast.operator) -> str:
        """
        Get the string symbol for an operator.

        Args:
            op: The operator AST node

        Returns:
            String representation of the operator
        """
        op_map = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.FloorDiv: "//",
            ast.Mod: "%",
            ast.Pow: "**",
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",
            ast.Is: "is",
            ast.IsNot: "is not",
            ast.In: "in",
            ast.NotIn: "not in",
            ast.And: "and",
            ast.Or: "or"
        }
        return op_map.get(type(op), type(op).__name__)

    def _get_name(self, node: ast.AST) -> str:
        """
        Get the name from a node that might be a Name or an Attribute.

        Args:
            node: The AST node

        Returns:
            The extracted name as a string
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return self._expr_to_str(node)
