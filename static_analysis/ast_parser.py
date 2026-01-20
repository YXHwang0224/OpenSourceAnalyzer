import ast
import os
import logging
from typing import List

class ASTFileInfo:
    """
    Store AST-related information for a single Python file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tree = None

    def parse(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                source = f.read()
            self.tree = ast.parse(source)
            logging.debug(f"Parsed AST for {self.file_path}")
        except Exception as e:
            logging.warning(f"Failed to parse {self.file_path}: {e}")
            self.tree = None


class ASTProjectParser:
    """
    Parse all Python files in a repository into ASTs.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.files: List[ASTFileInfo] = []

    def collect_python_files(self):
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(".py"):
                    self.files.append(ASTFileInfo(os.path.join(root, file)))

        logging.info(f"Collected {len(self.files)} Python files")

    def parse_all(self):
        for file_info in self.files:
            file_info.parse()

    def get_parsed_files(self) -> List[ASTFileInfo]:
        return [f for f in self.files if f.tree is not None]
