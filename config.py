"""
Global configuration for OpenSourceAnalyzer
"""

import os

# ===============================
# Repository settings
# ===============================
DEFAULT_BRANCH = "master"
REPO_BASE_DIR = "repos"

# ===============================
# Output directories
# ===============================
DATA_DIR = "data"
FIGURE_DIR = "figures"

# ===============================
# Analysis output files
# ===============================
COMMIT_CSV = os.path.join(DATA_DIR, "commits.csv")
BUG_COMMIT_CSV = os.path.join(DATA_DIR, "bug_commits.csv")
FUNCTION_METRICS_CSV = os.path.join(DATA_DIR, "functions.csv")
COMPLEXITY_CSV = os.path.join(DATA_DIR, "complexity.csv")
AUTHOR_CSV = os.path.join(DATA_DIR, "authors.csv")

# ===============================
# Visualization output files
# ===============================
COMMIT_FREQ_FIG = os.path.join(FIGURE_DIR, "commit_frequency.png")
BUG_RATIO_FIG = os.path.join(FIGURE_DIR, "bug_fix_ratio.png")
COMPLEXITY_DIST_FIG = os.path.join(FIGURE_DIR, "complexity_distribution.png")
AUTHOR_ACTIVITY_FIG = os.path.join(FIGURE_DIR, "author_activity.png")

# ===============================
# Thresholds
# ===============================
LONG_FUNCTION_THRESHOLD = 50
HIGH_COMPLEXITY_THRESHOLD = 10
ACTIVE_AUTHOR_THRESHOLD = 10
