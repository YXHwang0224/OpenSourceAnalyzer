import pandas as pd
import matplotlib.pyplot as plt
import logging

class ComplexityTrendPlotter:
    """
    Plot cyclomatic complexity trends.
    """

    def __init__(self, complexity_df: pd.DataFrame):
        self.df = complexity_df.copy()

    def plot_complexity_distribution(self, output_path: str = None):
        plt.figure(figsize=(8, 6))
        plt.hist(self.df["cyclomatic_complexity"], bins=20)
        plt.title("Cyclomatic Complexity Distribution")
        plt.xlabel("Complexity")
        plt.ylabel("Number of Functions")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            logging.info(f"Saved complexity distribution to {output_path}")
        else:
            plt.show()

    def plot_top_complex_functions(self, top_n: int = 10, output_path: str = None):
        top_df = (
            self.df
            .sort_values(by="cyclomatic_complexity", ascending=False)
            .head(top_n)
        )

        plt.figure(figsize=(10, 6))
        plt.barh(top_df["function"], top_df["cyclomatic_complexity"])
        plt.gca().invert_yaxis()
        plt.title(f"Top {top_n} Most Complex Functions")
        plt.xlabel("Cyclomatic Complexity")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path)
            logging.info(f"Saved top complexity plot to {output_path}")
        else:
            plt.show()
