import os
import sys
from git import Repo

def clone_repo(repo_url, output_dir):
    local_path = output_dir
    print(f"[repo_handler.py] 🧲 Checking if repo already cloned at {local_path}...", file=sys.stderr)
    if os.path.exists(os.path.join(local_path, ".git")):
        print("[repo_handler.py] ✅ Repo already cloned. Skipping clone. 😎", file=sys.stderr)
        return local_path
    print(f"[repo_handler.py] ⏳ Cloning repo from {repo_url}...", file=sys.stderr)
    Repo.clone_from(repo_url, local_path)
    print(f"[repo_handler.py] 🎉 Repo cloned to {local_path}!", file=sys.stderr)
    return local_path


### lldgen/file_parser.py
import os
from pathlib import Path

def parse_project_files(base_path):
    extensions = {".java", ".md", ".properties", ".yml", ".yaml"}
    files = []
    for root, _, filenames in os.walk(base_path):
        for file in filenames:
            if Path(file).suffix in extensions:
                files.append(os.path.join(root, file))
    return files
