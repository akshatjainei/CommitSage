import subprocess

def run_git_command(cmd, cwd=None):
    """Runs a git command and returns its output."""
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if result.returncode != 0:
        raise Exception(f"Error running command {' '.join(cmd)}: {result.stderr}")
    return result.stdout.strip()

def get_git_root(path):
    """Returns the root directory of the Git repository for the given path."""
    return run_git_command(["git", "rev-parse", "--show-toplevel"], cwd=path)

def get_staged_diff(path):
    """Gets the staged diff from the given repo path."""
    return run_git_command(["git", "diff", "--cached", "--unified=0"], cwd=path)

def get_staged_files(path):
    """Gets staged files from the given repo path."""
    output = run_git_command(["git", "diff", "--cached", "--name-only"], cwd=path)
    return output.splitlines()