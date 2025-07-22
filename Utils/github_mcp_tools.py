from langchain.tools import Tool
from typing import Dict, List, Any
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools


class GitHubMCPToolkit:
    """
    Toolkit for working with GitHub MCP Server tools
    """
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token
        self.mcp_server_params = StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-github",
                "--github-token", github_token if github_token else ""
            ]
        )
        self._tools_cache = None
    
    async def get_tools(self) -> List[Tool]:
        """Get all available GitHub MCP tools"""
        if self._tools_cache is None:
            async with stdio_client(self.mcp_server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self._tools_cache = await load_mcp_tools(session)
        return self._tools_cache
    
    async def get_pull_request(self, owner: str, repo: str, pull_number: int) -> Dict:
        """Get pull request details"""
        tools = await self.get_tools()
        pr_tool = next((tool for tool in tools if 'pull' in tool.name.lower()), None)
        
        if pr_tool:
            return await pr_tool.ainvoke({
                "owner": owner,
                "repo": repo,
                "pull_number": pull_number
            })
        else:
            raise Exception("Pull request tool not found")
    
    async def get_repository_files(self, owner: str, repo: str, path: str = "") -> List[Dict]:
        """Get repository file contents"""
        tools = await self.get_tools()
        files_tool = next((tool for tool in tools if 'files' in tool.name.lower() or 'content' in tool.name.lower()), None)
        
        if files_tool:
            return await files_tool.ainvoke({
                "owner": owner,
                "repo": repo,
                "path": path
            })
        else:
            raise Exception("Files tool not found")
    
    async def create_issue_comment(self, owner: str, repo: str, issue_number: int, body: str) -> Dict:
        """Create a comment on an issue or pull request"""
        tools = await self.get_tools()
        comment_tool = next((tool for tool in tools if 'comment' in tool.name.lower()), None)
        
        if comment_tool:
            return await comment_tool.ainvoke({
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number,
                "body": body
            })
        else:
            raise Exception("Comment tool not found")
    
    async def list_tools(self) -> List[str]:
        """List all available GitHub MCP tools"""
        tools = await self.get_tools()
        return [tool.name for tool in tools]


# Create LangChain-compatible tools
def create_github_mcp_tools(github_token: str = None) -> List[Tool]:
    """
    Create LangChain-compatible tools from GitHub MCP Server
    """
    toolkit = GitHubMCPToolkit(github_token)
    
    async def get_pr_wrapper(input_str: str) -> str:
        """Wrapper for getting PR data"""
        try:
            # Parse input (expected format: "owner/repo#pr_number")
            if '#' in input_str:
                repo_part, pr_number = input_str.split('#')
                owner, repo = repo_part.split('/')
                pr_data = await toolkit.get_pull_request(owner, repo, int(pr_number))
                return str(pr_data)
            else:
                return "Invalid input format. Use: owner/repo#pr_number"
        except Exception as e:
            return f"Error: {e}"
    
    async def get_files_wrapper(input_str: str) -> str:
        """Wrapper for getting repository files"""
        try:
            # Parse input (expected format: "owner/repo:path")
            if ':' in input_str:
                repo_part, path = input_str.split(':', 1)
                owner, repo = repo_part.split('/')
                files = await toolkit.get_repository_files(owner, repo, path)
                return str(files)
            else:
                # No path specified
                owner, repo = input_str.split('/')
                files = await toolkit.get_repository_files(owner, repo)
                return str(files)
        except Exception as e:
            return f"Error: {e}"
    
    def sync_get_pr(input_str: str) -> str:
        """Synchronous wrapper for get_pr_wrapper"""
        return asyncio.run(get_pr_wrapper(input_str))
    
    def sync_get_files(input_str: str) -> str:
        """Synchronous wrapper for get_files_wrapper"""
        return asyncio.run(get_files_wrapper(input_str))
    
    return [
        Tool(
            name="github_get_pull_request",
            func=sync_get_pr,
            description="Get pull request details from GitHub. Input format: 'owner/repo#pr_number' (e.g., 'microsoft/vscode#123')"
        ),
        Tool(
            name="github_get_repository_files",
            func=sync_get_files,
            description="Get repository files from GitHub. Input format: 'owner/repo:path' (e.g., 'microsoft/vscode:src/main.py'). Omit ':path' to get root directory."
        )
    ]
