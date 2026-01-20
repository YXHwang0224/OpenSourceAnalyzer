import pandas as pd
from git_analyzer.bug_detector import BugDetector

def test_bug_fix_detection():
    df = pd.DataFrame([
        {"message": "fix bug in parser"},
        {"message": "add new feature"}
    ])

    detector = BugDetector(df)
    result = detector.detect()

    assert result["is_bug_fix"].iloc[0] is True
    assert result["is_bug_fix"].iloc[1] is False
