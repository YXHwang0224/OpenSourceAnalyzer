import os
from git_analyzer.repo_loader import RepoLoader

def test_repo_name_from_url():
    loader = RepoLoader(base_dir="repos_test")
    name = loader._repo_name_from_url("https://github.com/psf/requests.git")
    assert name == "requests"

def test_repo_base_dir_created(tmp_path):
    base = tmp_path / "repos"
    loader = RepoLoader(base_dir=str(base))
    assert os.path.exists(base)
