import ast
from static_analysis.complexity import CyclomaticComplexityVisitor

def test_cyclomatic_complexity():
    code = """
def foo(x):
    if x > 0:
        return x
    else:
        return -x
"""
    tree = ast.parse(code)
    visitor = CyclomaticComplexityVisitor("dummy.py")
    visitor.visit(tree)

    assert visitor.results[0]["cyclomatic_complexity"] >= 2
