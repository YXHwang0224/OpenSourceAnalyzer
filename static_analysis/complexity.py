import ast
import pandas as pd
import logging

class CyclomaticComplexityVisitor(ast.NodeVisitor):
    """
    Compute cyclomatic complexity for functions.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.results = []
        self.current_function = None
        self.complexity = 0

    def generic_visit(self, node):
        if isinstance(node, (
            ast.If, ast.For, ast.While, ast.And, ast.Or,
            ast.ExceptHandler, ast.With, ast.Try
        )):
            self.complexity += 1
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.complexity = 1
        self.generic_visit(node)

        self.results.append({
            "file": self.file_path,
            "function": node.name,
            "lineno": node.lineno,
            "cyclomatic_complexity": self.complexity
        })

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)


class ComplexityAnalyzer:
    """
    Analyze cyclomatic complexity across project.
    """

    def analyze(self, parsed_files):
        all_results = []

        for file_info in parsed_files:
            visitor = CyclomaticComplexityVisitor(file_info.file_path)
            visitor.visit(file_info.tree)
            all_results.extend(visitor.results)

        df = pd.DataFrame(all_results)
        logging.info(f"Computed complexity for {len(df)} functions")
        return df
