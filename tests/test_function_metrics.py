import ast
from static_analysis.function_metrics import FunctionMetricVisitor

def test_function_metric_visitor():
    code = """
def foo(a, b):
    return a + b
"""
    tree = ast.parse(code)
    visitor = FunctionMetricVisitor("dummy.py")
    visitor.visit(tree)

    assert len(visitor.records) == 1
    record = visitor.records[0]
    assert record["function"] == "foo"
    assert record["args"] == 2
