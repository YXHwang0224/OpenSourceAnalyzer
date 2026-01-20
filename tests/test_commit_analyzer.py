import pandas as pd
from git_analyzer.commit_analyzer import CommitAnalyzer

class DummyCommitAnalyzer(CommitAnalyzer):
    def analyze(self):
        self.commits_df = pd.DataFrame([
            {
                "hash": "abc",
                "author_name": "Alice",
                "author_email": "a@test.com",
                "date": "2024-01-01",
                "message": "initial commit",
                "files_changed": 1,
                "insertions": 10,
                "deletions": 0,
                "lines_changed": 10,
                "merge": False
            }
        ])
        return self.commits_df

def test_commit_dataframe_structure():
    analyzer = DummyCommitAnalyzer("dummy")
    df = analyzer.analyze()
    assert "hash" in df.columns
    assert "author_name" in df.columns
    assert len(df) == 1
