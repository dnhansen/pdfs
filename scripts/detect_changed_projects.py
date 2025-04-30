import os
import yaml
import subprocess
import json

PUBLISH_BRANCH = "publish"
PDF_REPO_ROOT = os.getcwd()
PROJECTS_DIR = os.path.join(PDF_REPO_ROOT, "projects")
OUTPUT_VAR = "matrix"

def update_metadata(path, new_data):
    with open(path, "w") as f:
        yaml.dump(new_data, f)

def get_commit_hash(repo_url, branch):
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--heads", repo_url, branch],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        if result.stdout.strip():
            return result.stdout.split()[0]
    except subprocess.CalledProcessError:
        pass
    return None

def main():
    changed = []
    for project in os.listdir(PROJECTS_DIR):
        metadata_path = os.path.join(PROJECTS_DIR, project, "metadata.yaml")
        if not os.path.isfile(metadata_path):
            print(f"[SKIP] {project}: no metadata")
            continue
        
        with open(metadata_path, "r") as f:
            metadata = yaml.safe_load(f)
        
        repo = metadata["repo"]
        branch = metadata.get("branch", PUBLISH_BRANCH)
        known_commit = metadata.get("commit", None)
        newest_commit = get_commit_hash(repo, branch)

        if not newest_commit:
            print(f"[SKIP] {project}: no publish branch")
            continue
        if known_commit != newest_commit:
            print(f"[BUILD] {project}: new commit {newest_commit}")
            changed.append(project)
            metadata["commit"] = newest_commit
            update_metadata(metadata_path, metadata)
        else:
            print(f"[SKIP] {project}: up to date")

    # Output changed project list to GitHub Actions
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a") as f:
            f.write(f"{OUTPUT_VAR}={json.dumps(changed)}\n")
    else:
        print(json.dumps(changed))  # For local testing

if __name__ == "__main__":
    main()