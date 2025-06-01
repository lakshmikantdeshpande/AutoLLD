import os
import sys
from pathlib import Path

def parse_project_files(base_path):
    print(f"[file_parser.py] 🔍 Scanning for project files in {base_path}...", file=sys.stderr)
    extensions = {".java", ".md", ".properties", ".yml", ".yaml"}
    files = []
    for root, _, filenames in os.walk(base_path):
        for file in filenames:
            if Path(file).suffix in extensions:
                files.append(os.path.join(root, file))
    print(f"[file_parser.py] 📄 Found {len(files)} files with relevant extensions!", file=sys.stderr)
    return files
