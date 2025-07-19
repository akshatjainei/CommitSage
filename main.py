import os
from pathlib import Path
import argparse
import sys
from Utils.git_util import(
    get_git_root,
    get_staged_diff,
    get_staged_files
)

def main():
    parser = argparse.ArgumentParser(description="Generate commit context from staged git changes.")
    parser.add_argument(
        "path",
        nargs="?",
        default=os.getcwd(),
        help="Path to the Git repository (default: current directory)"
    )

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    if not target_path.exists():
        print(f"Path does not exist: {target_path}")
        sys.exit(1)

    try:
        git_root = get_git_root(target_path)
        print(f"Git root detected at: {git_root}\n")

        staged_files = get_staged_files(git_root)
        if not staged_files:
            print("No staged files found")
            return

        print("Staged files:")
        for file in staged_files:
            print(f" - {file}")

        print("\nFetching staged diff...\n")
        diff_output = get_staged_diff(git_root)
        print(diff_output)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
