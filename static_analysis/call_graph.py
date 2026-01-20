import ast
import logging
from collections import defaultdict

class CallGraphVisitor(ast.NodeVisitor):
    """
    Build function call graph using AST.
    """

    def __init__(self):
        self.current_function = None
        self.calls = defaultdict(set)

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                self.calls[self.current_function].add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                self.calls[self.current_function].add(node.func.attr)
        self.generic_visit(node)


class CallGraphAnalyzer:
    """
    Analyze call graph for a project.
    """

    def analyze(self, parsed_files):
        graph = defaultdict(set)

        for file_info in parsed_files:
            visitor = CallGraphVisitor()
            visitor.visit(file_info.tree)
            for caller, callees in visitor.calls.items():
                graph[caller].update(callees)

        logging.info(f"Constructed call graph with {len(graph)} functions")
        return graph
