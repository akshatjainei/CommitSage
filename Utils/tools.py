from langchain.tools import Tool
from Utils import git_util
from Utils import diff_parser

# Tool: Get Git Root
get_git_root_tool = Tool(
    name="get_git_root",
    func=git_util.get_git_root,
    description="Get the root directory of the Git repository for a given path. Input: path to a directory inside the repo. Output: root path as string."
)

# Tool: Get Staged Diff
get_staged_diff_tool = Tool(
    name="get_staged_diff",
    func=git_util.get_staged_diff,
    description="Get the staged diff (unified format) for a given repo path. Input: path to the repo. Output: diff as string."
)

# Tool: Get Staged Files
get_staged_files_tool = Tool(
    name="get_staged_files",
    func=git_util.get_staged_files,
    description="Get the list of staged files for a given repo path. Input: path to the repo. Output: list of file names."
)

# Tool: Parse Diff
parse_diff_tool = Tool(
    name="parse_diff",
    func=diff_parser.parse_diff,
    description="Parse a unified diff and summarize changes per file. Input: diff as string. Output: dict of file to list of changes."
)

all_tools = [
    get_git_root_tool,
    get_staged_diff_tool,
    get_staged_files_tool,
    parse_diff_tool
] 