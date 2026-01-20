import pandas as pd
import matplotlib.pyplot as plt
import logging

class BugFixPlotter:
    """
    Visualize bug-fix commit statistics.
    """

    def __init__(self, commit_df: pd.DataFrame):
        self.df = commit_df.copy()
        if "is_bug_fix" not in self.df.columns:
            raise ValueError("commit_df must contain 'is_bug_fix' column")
        self.df["date"] = pd.to_datetime(self.df["date"], utc=True).dt.tz_localize(None)

    def plot_ratio_pie(self, output_path: str = None):
        counts = self.df["is_bug_fix"].value_counts()
        labels = ["Bug Fix Commits", "Other Commits"]

        plt.figure(figsize=(6, 6))
        plt.pie(
            [counts.get(True, 0), counts.get(False, 0)],
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Bug Fix Commit Ratio")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            logging.info(f"Saved bug-fix ratio pie chart to {output_path}")
        else:
            plt.show()

    def plot_bug_fix_over_time(self, output_path: str = None):
        ts = (
            self.df[self.df["is_bug_fix"]]
            .set_index("date")
            .resample("M")
            .size()
        )

        plt.figure(figsize=(12, 6))
        plt.plot(ts.index, ts.values)
        plt.title("Bug Fix Commits Over Time")
        plt.xlabel("Time")
        plt.ylabel("Bug Fix Commits")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            logging.info(f"Saved bug-fix trend plot to {output_path}")
        else:
            plt.show()
