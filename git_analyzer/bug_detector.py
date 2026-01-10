import pandas as pd
import re
import logging

class BugDetector:
    """
    Detect bug-fix related commits using commit messages.
    """

    BUG_KEYWORDS = [
        "fix", "bug", "error", "issue", "fault", "defect",
        "crash", "incorrect", "wrong", "patch"
    ]

    def __init__(self, commit_df: pd.DataFrame):
        self.commit_df = commit_df.copy()

    def _is_bug_fix(self, message: str) -> bool:
        msg = message.lower()
        for kw in self.BUG_KEYWORDS:
            if re.search(rf"\b{kw}\b", msg):
                return True
        return False

    def detect(self) -> pd.DataFrame:
        """
        Add bug_fix flag to commit dataframe.
        """
        self.commit_df["is_bug_fix"] = self.commit_df["message"].apply(self._is_bug_fix)
        bug_count = self.commit_df["is_bug_fix"].sum()
        logging.info(f"Detected {bug_count} bug-fix commits")
        return self.commit_df

    def bug_fix_ratio(self) -> float:
        """
        Calculate ratio of bug-fix commits.
        """
        total = len(self.commit_df)
        bug_fixes = self.commit_df["is_bug_fix"].sum()
        return bug_fixes / total if total > 0 else 0.0
