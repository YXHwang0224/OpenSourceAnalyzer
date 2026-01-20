import pandas as pd
from pydriller import Repository
from datetime import datetime
import logging

class CommitAnalyzer:
    """
    Analyze commit-level information of a Git repository.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.commits_df = None

    def _analyze_single_commit(self, commit):
        """
        Extract information from a single commit object.
        """
        return {
            "hash": commit.hash,
            "author_name": commit.author.name,
            "author_email": commit.author.email,
            "date": commit.author_date,
            "message": commit.msg.strip(),
            "files_changed": commit.files,
            "insertions": commit.insertions,
            "deletions": commit.deletions,
            "lines_changed": commit.insertions + commit.deletions,
            "merge": commit.merge
        }

    def analyze(self) -> pd.DataFrame:
        """
        Traverse all commits and build a DataFrame.
        """
        records = []
        logging.info("Start traversing commits")

        for commit in Repository(self.repo_path).traverse_commits():
            try:
                record = self._analyze_single_commit(commit)
                records.append(record)
            except Exception as e:
                logging.warning(f"Failed to analyze commit {commit.hash}: {e}")

        self.commits_df = pd.DataFrame(records)
        logging.info(f"Total commits analyzed: {len(self.commits_df)}")
        return self.commits_df

    def save_to_csv(self, output_path: str):
        if self.commits_df is not None:
            self.commits_df.to_csv(output_path, index=False)
            logging.info(f"Commit data saved to {output_path}")

    def commits_per_day(self) -> pd.DataFrame:
        """
        Aggregate commits by day.
        """
        df = self.commits_df.copy()
        df["date"] = pd.to_datetime(df["date"]).dt.date
        return df.groupby("date").size().reset_index(name="commit_count")

    def commits_per_month(self) -> pd.DataFrame:
        """
        Aggregate commits by month.
        """
        df = self.commits_df.copy()
        df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
        return df.groupby("month").size().reset_index(name="commit_count")
