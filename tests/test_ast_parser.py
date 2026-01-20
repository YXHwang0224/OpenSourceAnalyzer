import tempfile
import os
from static_analysis.ast_parser import ASTProjectParser

def test_ast_parsing_single_file():
    with tempfile.TemporaryDirectory() as tmp:
        file_path = os.path.join(tmp, "test.py")
        with open(file_path, "w") as f:
            f.write("def foo():\n    return 1\n")

        parser = ASTProjectParser(tmp)
        parser.collect_python_files()
        parser.parse_all()

        parsed = parser.get_parsed_files()
        assert len(parsed) == 1
        assert parsed[0].tree is not None
