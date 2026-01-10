from pydriller import Repository
import pandas as pd
import logging
import os

class DiffAnalyzer:
    """
    Analyze file-level and line-level changes in commits.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def analyze_diffs(self) -> pd.DataFrame:
        """
        Collect diff statistics for each modified file.
        """
        records = []
        logging.info("Start diff analysis")

        for commit in Repository(self.repo_path).traverse_commits():
            for mod in commit.modified_files:
                record = {
                    "commit_hash": commit.hash,
                    "file_path": mod.new_path or mod.old_path,
                    "change_type": mod.change_type.name,
                    "added_lines": mod.added_lines,
                    "deleted_lines": mod.deleted_lines,
                    "nloc": mod.nloc,
                    "complexity": mod.complexity
                }
                records.append(record)

        df = pd.DataFrame(records)
        logging.info(f"Total file diffs analyzed: {len(df)}")
        return df

    def filter_python_files(self, diff_df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter diffs to only Python files.
        """
        return diff_df[diff_df["file_path"].str.endswith(".py", na=False)]

    def summarize_changes(self, diff_df: pd.DataFrame) -> pd.DataFrame:
        """
        Summarize changes per file.
        """
        return diff_df.groupby("file_path").agg({
            "added_lines": "sum",
            "deleted_lines": "sum"
        }).reset_index()
