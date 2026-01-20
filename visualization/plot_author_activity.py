import pandas as pd
import matplotlib.pyplot as plt
import logging

class AuthorActivityPlotter:
    """
    Visualize author contribution activity.
    """

    def __init__(self, author_df: pd.DataFrame):
        self.df = author_df.copy()

    def plot_commit_count(self, top_n: int = 10, output_path: str = None):
        top_df = self.df.head(top_n)

        plt.figure(figsize=(10, 6))
        plt.bar(top_df["author_name"], top_df["commit_count"])
        plt.xticks(rotation=45, ha="right")
        plt.title(f"Top {top_n} Authors by Commit Count")
        plt.xlabel("Author")
        plt.ylabel("Commits")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            logging.info(f"Saved author activity plot to {output_path}")
        else:
            plt.show()
