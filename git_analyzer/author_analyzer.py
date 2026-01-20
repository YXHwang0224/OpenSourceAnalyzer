import pandas as pd
import logging

class AuthorAnalyzer:
    """
    Analyze author contribution patterns.
    """

    def __init__(self, commit_df: pd.DataFrame):
        self.commit_df = commit_df

    def commits_by_author(self) -> pd.DataFrame:
        """
        Count commits per author.
        """
        result = (
            self.commit_df
            .groupby("author_name")
            .size()
            .reset_index(name="commit_count")
            .sort_values(by="commit_count", ascending=False)
        )
        logging.info("Computed commits per author")
        return result

    def lines_changed_by_author(self) -> pd.DataFrame:
        """
        Sum changed lines per author.
        """
        result = (
            self.commit_df
            .groupby("author_name")["lines_changed"]
            .sum()
            .reset_index()
            .sort_values(by="lines_changed", ascending=False)
        )
        logging.info("Computed lines changed per author")
        return result

    def active_authors(self, threshold: int = 10) -> pd.DataFrame:
        """
        Identify active authors based on commit count threshold.
        """
        df = self.commits_by_author()
        return df[df["commit_count"] >= threshold]
