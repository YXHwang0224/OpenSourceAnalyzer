import pandas as pd
from git_analyzer.author_analyzer import AuthorAnalyzer

def test_commits_by_author():
    df = pd.DataFrame([
        {"author_name": "Alice", "lines_changed": 10},
        {"author_name": "Alice", "lines_changed": 5},
        {"author_name": "Bob", "lines_changed": 20}
    ])

    analyzer = AuthorAnalyzer(df)
    result = analyzer.commits_by_author()

    assert result.iloc[0]["author_name"] == "Alice"
    assert result.iloc[0]["commit_count"] == 2
