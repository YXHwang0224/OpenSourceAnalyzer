import pandas as pd
import logging

class CodeSmellDetector:
    """
    Detect simple code smells based on static metrics.
    """

    def __init__(self, function_df: pd.DataFrame, complexity_df: pd.DataFrame):
        self.function_df = function_df
        self.complexity_df = complexity_df

    def detect_long_functions(self, length_threshold: int = 50):
        df = self.function_df[
            self.function_df["body_length"] > length_threshold
        ].copy()
        df["smell"] = "Long Function"
        logging.info(f"Detected {len(df)} long functions")
        return df

    def detect_high_complexity(self, complexity_threshold: int = 10):
        df = self.complexity_df[
            self.complexity_df["cyclomatic_complexity"] > complexity_threshold
        ].copy()
        df["smell"] = "High Complexity"
        logging.info(f"Detected {len(df)} high complexity functions")
        return df

    def detect_all(self):
        smells = []

        smells.append(self.detect_long_functions())
        smells.append(self.detect_high_complexity())

        result = pd.concat(smells, ignore_index=True)
        logging.info(f"Total code smells detected: {len(result)}")
        return result
