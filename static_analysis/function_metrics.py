import ast
import pandas as pd
import logging

class FunctionMetricVisitor(ast.NodeVisitor):
    """
    Collect function-level metrics using AST traversal.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.records = []

    def visit_FunctionDef(self, node):
        record = {
            "file": self.file_path,
            "function": node.name,
            "lineno": node.lineno,
            "args": len(node.args.args),
            "body_length": len(node.body),
            "has_return": any(isinstance(n, ast.Return) for n in ast.walk(node)),
            "has_docstring": ast.get_docstring(node) is not None
        }
        self.records.append(record)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)


class FunctionMetricsAnalyzer:
    """
    Analyze function-level metrics across a project.
    """

    def __init__(self):
        self.df = pd.DataFrame()

    def analyze(self, parsed_files):
        all_records = []

        for file_info in parsed_files:
            visitor = FunctionMetricVisitor(file_info.file_path)
            visitor.visit(file_info.tree)
            all_records.extend(visitor.records)

        self.df = pd.DataFrame(all_records)
        logging.info(f"Extracted metrics for {len(self.df)} functions")
        return self.df

    def save_to_csv(self, path: str):
        if not self.df.empty:
            self.df.to_csv(path, index=False)
            logging.info(f"Function metrics saved to {path}")
