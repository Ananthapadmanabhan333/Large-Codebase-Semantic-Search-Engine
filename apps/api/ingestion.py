import os
import git
import shutil
import uuid
from typing import List, Dict
from pathlib import Path

class IngestionEngine:
    def __init__(self, storage_path: str = "./storage/repos"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def clone_repository(self, repo_url: str, branch: str = "main") -> str:
        """
        Clones a repository and returns the local path.
        """
        repo_id = str(uuid.uuid4())
        local_path = self.storage_path / repo_id
        
        print(f"Cloning {repo_url} to {local_path}...")
        
        try:
            git.Repo.clone_from(
                repo_url, 
                local_path, 
                branch=branch, 
                depth=1,  # Shallow clone for speed
                single_branch=True
            )
            return str(local_path)
        except Exception as e:
            print(f"Failed to clone repository: {e}")
            raise

    def walk_repository(self, local_path: str) -> List[Dict]:
        """
        Walks the repository and returns a list of files with metadata.
        """
        repo_path = Path(local_path)
        files_metadata = []

        for path in repo_path.rglob('*'):
            if path.is_file() and not self._is_ignored(path):
                relative_path = path.relative_to(repo_path)
                files_metadata.append({
                    "name": path.name,
                    "path": str(relative_path),
                    "full_path": str(path),
                    "extension": path.suffix,
                    "size": path.stat().st_size
                })
        
        return files_metadata

    def _is_ignored(self, path: Path) -> bool:
        """
        Basic ignore logic (can be extended with .gitignore parsing).
        """
        ignored_dirs = {'.git', 'node_modules', '__pycache__', 'dist', 'build', 'venv', '.env'}
        for part in path.parts:
            if part in ignored_dirs:
                return True
        return False

    def cleanup(self, local_path: str):
        """
        Removes the local clone.
        """
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
