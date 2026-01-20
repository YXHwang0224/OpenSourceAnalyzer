import pandas as pd
import matplotlib.pyplot as plt
import logging

class CommitFrequencyPlotter:
    """
    Plot commit frequency over time.
    """

    def __init__(self, commit_df: pd.DataFrame):
        self.df = commit_df.copy()
        self.df["date"] = pd.to_datetime(self.df["date"], utc=True).dt.tz_localize(None)

    def plot_daily(self, output_path: str = None):
        daily = (
            self.df
            .set_index("date")
            .resample("D")
            .size()
        )

        plt.figure(figsize=(12, 6))
        plt.plot(daily.index, daily.values)
        plt.title("Daily Commit Frequency")
        plt.xlabel("Date")
        plt.ylabel("Number of Commits")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            logging.info(f"Saved daily commit plot to {output_path}")
        else:
            plt.show()

    def plot_monthly(self, output_path: str = None):
        monthly = (
            self.df
            .set_index("date")
            .resample("M")
            .size()
        )

        plt.figure(figsize=(12, 6))
        plt.bar(monthly.index.astype(str), monthly.values)
        plt.xticks(rotation=45)
        plt.title("Monthly Commit Frequency")
        plt.xlabel("Month")
        plt.ylabel("Number of Commits")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            logging.info(f"Saved monthly commit plot to {output_path}")
        else:
            plt.show()
