import pandas as pd
import logging

class TimeSeriesAnalyzer:
    """
    Perform time series analysis on commit history.
    """

    def __init__(self, commit_df: pd.DataFrame):
        self.df = commit_df.copy()
        self.df["date"] = pd.to_datetime(self.df["date"])

    def commits_over_time(self, freq: str = "M") -> pd.DataFrame:
        """
        Aggregate commits over time.
        freq: D (day), W (week), M (month)
        """
        ts = (
            self.df
            .set_index("date")
            .resample(freq)
            .size()
            .reset_index(name="commit_count")
        )
        logging.info(f"Generated commit time series with freq={freq}")
        return ts

    def bug_fix_over_time(self, freq: str = "M") -> pd.DataFrame:
        """
        Aggregate bug-fix commits over time.
        """
        bug_df = self.df[self.df.get("is_bug_fix", False)]
        ts = (
            bug_df
            .set_index("date")
            .resample(freq)
            .size()
            .reset_index(name="bug_fix_count")
        )
        logging.info("Generated bug-fix time series")
        return ts
