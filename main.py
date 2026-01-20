import argparse
import os
import logging

from git_analyzer.repo_loader import RepoLoader
from git_analyzer.commit_analyzer import CommitAnalyzer
from git_analyzer.diff_analyzer import DiffAnalyzer
from git_analyzer.author_analyzer import AuthorAnalyzer
from git_analyzer.bug_detector import BugDetector
from git_analyzer.time_series import TimeSeriesAnalyzer

from static_analysis.ast_parser import ASTProjectParser
from static_analysis.function_metrics import FunctionMetricsAnalyzer
from static_analysis.complexity import ComplexityAnalyzer
from static_analysis.code_smell import CodeSmellDetector

from visualization.plot_commit_frequency import CommitFrequencyPlotter
from visualization.plot_bug_fix_ratio import BugFixPlotter
from visualization.plot_complexity_trend import ComplexityTrendPlotter
from visualization.plot_author_activity import AuthorActivityPlotter

import config


def setup_environment():
    """
    Create necessary directories.
    """
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.FIGURE_DIR, exist_ok=True)
    os.makedirs(config.REPO_BASE_DIR, exist_ok=True)


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Open Source Software Evolution Analyzer"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="GitHub repository URL"
    )
    parser.add_argument(
        "--branch",
        type=str,
        default=None,
        help="Git branch name (default: repository default branch)"
    )
    return parser.parse_args()


def main():
    setup_logger()
    setup_environment()
    args = parse_args()

    logging.info("=== Open Source Analyzer Started ===")

    # -------------------------------
    # Step 1: Clone repository
    # -------------------------------
    loader = RepoLoader(config.REPO_BASE_DIR)
    repo_path = loader.clone_repo(args.repo, args.branch)

    # -------------------------------
    # Step 2: Commit analysis
    # -------------------------------
    commit_analyzer = CommitAnalyzer(repo_path)
    commit_df = commit_analyzer.analyze()
    commit_analyzer.save_to_csv(config.COMMIT_CSV)

    # -------------------------------
    # Step 3: Bug fix detection
    # -------------------------------
    bug_detector = BugDetector(commit_df)
    commit_df = bug_detector.detect()
    commit_df.to_csv(config.BUG_COMMIT_CSV, index=False)

    # -------------------------------
    # Step 4: Author analysis
    # -------------------------------
    author_analyzer = AuthorAnalyzer(commit_df)
    author_df = author_analyzer.commits_by_author()
    author_df.to_csv(config.AUTHOR_CSV, index=False)

    # -------------------------------
    # Step 5: Static analysis (AST)
    # -------------------------------
    parser = ASTProjectParser(repo_path)
    parser.collect_python_files()
    parser.parse_all()
    parsed_files = parser.get_parsed_files()

    func_analyzer = FunctionMetricsAnalyzer()
    func_df = func_analyzer.analyze(parsed_files)
    func_analyzer.save_to_csv(config.FUNCTION_METRICS_CSV)

    complexity_analyzer = ComplexityAnalyzer()
    complexity_df = complexity_analyzer.analyze(parsed_files)
    complexity_df.to_csv(config.COMPLEXITY_CSV, index=False)

    # -------------------------------
    # Step 6: Code smell detection
    # -------------------------------
    smell_detector = CodeSmellDetector(func_df, complexity_df)
    smells_df = smell_detector.detect_all()
    logging.info(f"Detected {len(smells_df)} code smells")

    # -------------------------------
    # Step 7: Visualization
    # -------------------------------
    CommitFrequencyPlotter(commit_df).plot_monthly(
        config.COMMIT_FREQ_FIG
    )

    BugFixPlotter(commit_df).plot_ratio_pie(
        config.BUG_RATIO_FIG
    )

    ComplexityTrendPlotter(complexity_df).plot_complexity_distribution(
        config.COMPLEXITY_DIST_FIG
    )

    AuthorActivityPlotter(author_df).plot_commit_count(
        output_path=config.AUTHOR_ACTIVITY_FIG
    )

    logging.info("=== Analysis Completed Successfully ===")
    logging.info(f"Results saved in '{config.DATA_DIR}' and '{config.FIGURE_DIR}'")


if __name__ == "__main__":
    main()
