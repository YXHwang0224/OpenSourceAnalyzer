import os
import shutil
from git import Repo, GitCommandError
import logging

class RepoLoader:
    """
    Responsible for cloning and managing Git repositories.
    """

    def __init__(self, base_dir: str = "repos"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _repo_name_from_url(self, repo_url: str) -> str:
        name = repo_url.rstrip("/").split("/")[-1]
        return name.replace(".git", "")

    def clone_repo(self, repo_url: str, branch: str | None = None) -> str:
        """
        Clone a GitHub repository if not exists.
        If branch is None, use repository default branch (main/master).
        """
        repo_name = self._repo_name_from_url(repo_url)
        local_path = os.path.join(self.base_dir, repo_name)

        if os.path.exists(local_path):
            logging.info(f"Repository already exists: {local_path}")
            return local_path

        try:
            logging.info(f"Cloning repository: {repo_url}")

            if branch:
                logging.info(f"Using specified branch: {branch}")
                Repo.clone_from(repo_url, local_path, branch=branch)
            else:
                logging.info("Using repository default branch")
                Repo.clone_from(repo_url, local_path)

            logging.info("Clone completed")
            return local_path

        except GitCommandError as e:
            logging.error(f"Clone failed: {e}")
            raise
        
    def remove_repo(self, repo_path: str):
        """
        Remove a cloned repository.
        """
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
            logging.info(f"Removed repository: {repo_path}")
