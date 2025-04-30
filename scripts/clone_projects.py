import os
import yaml
import subprocess

PDF_REPO_ROOT = os.getcwd()
PROJECTS_DIR = os.path.join(PDF_REPO_ROOT, "projects")
TEMP_DIR = os.path.join(PDF_REPO_ROOT, "tmp")
# os.makedirs(PROJECTS_DIR, exist_ok=True)

for project_folder in os.listdir(PROJECTS_DIR):
    metadata_path = os.path.join(PROJECTS_DIR, project_folder, "metadata.yaml")
    if not os.path.isfile(metadata_path):
        continue
    
    with open(metadata_path, "r") as f:
        metadata = yaml.safe_load(f)
    
    repo = metadata["repo"]
    branch = metadata.get("branch", "publish")
    name = project_folder
    dest_dir = os.path.join(TEMP_DIR, name)

    print(f"Cloning {repo} (branch: {branch}) into {dest_dir}")
    subprocess.run([
        "git", "clone", "--depth", "1", "--branch", branch, repo, dest_dir
    ], check=True)