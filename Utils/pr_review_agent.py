import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate
from langchain.schema import HumanMessage, SystemMessage


@dataclass
class PRAnalysis:
    """Data class to hold PR analysis results"""
    summary: str
    best_practices: List[str]
    potential_issues: List[str]
    security_concerns: List[str]
    performance_insights: List[str]
    code_quality_score: int
    recommendations: List[str]
    review_comment: str


class PRReviewAgent:
    """
    PR Review Agent that uses GitHub MCP Server to analyze pull requests
    and provide comprehensive feedback including best practices, potential issues,
    and security concerns.
    """
    
    def __init__(self, openai_api_key: str, github_token: str = None):
        self.llm = ChatOpenAI(
            temperature=0.3, 
            model="gpt-4o-mini",
            api_key=openai_api_key
        )
        self.github_token = github_token
        
        # GitHub MCP Server configuration
        self.mcp_server_params = StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-github",
                "--github-token", github_token if github_token else ""
            ]
        )
        
        # Analysis prompts
        self.system_prompt = SystemMessagePromptTemplate.from_template("""
You are an expert code reviewer with extensive experience in software engineering best practices, 
security, performance optimization, and code quality. You analyze pull requests thoroughly and 
provide actionable feedback.

Your analysis should cover:
1. Code quality and adherence to best practices
2. Potential bugs, errors, or logical issues
3. Security vulnerabilities or concerns
4. Performance implications
5. Maintainability and readability
6. Testing coverage and quality
7. Documentation completeness

Be constructive, specific, and provide concrete suggestions for improvement.
""")
        
        self.analysis_prompt = PromptTemplate(
            input_variables=["pr_data", "diff_content", "file_contents"],
            template="""
Analyze the following pull request:

## PR Information:
{pr_data}

## Code Changes:
{diff_content}

## File Contents:
{file_contents}

Provide a comprehensive analysis covering:

1. **Summary**: Brief overview of the changes
2. **Best Practices**: What the PR does well
3. **Issues**: Potential problems, bugs, or concerns
4. **Security**: Security implications or vulnerabilities
5. **Performance**: Performance considerations
6. **Recommendations**: Specific improvement suggestions
7. **Quality Score**: Rate the code quality from 1-10

Format your response as a structured analysis.
"""
        )
        
        self.comment_prompt = PromptTemplate(
            input_variables=["analysis"],
            template="""
Based on this analysis: {analysis}

Generate a constructive and professional PR review comment that:
- Acknowledges good practices
- Clearly explains issues and concerns
- Provides specific, actionable recommendations
- Maintains a collaborative and helpful tone
- Uses markdown formatting for clarity

The comment should be suitable for posting directly on a GitHub PR.
"""
        )

    async def analyze_pr(self, owner: str, repo: str, pr_number: int) -> PRAnalysis:
        """
        Analyze a pull request using GitHub MCP Server
        
        Args:
            owner: Repository owner
            repo: Repository name
            pr_number: Pull request number
            
        Returns:
            PRAnalysis object with comprehensive analysis
        """
        async with stdio_client(self.mcp_server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)
                
                # Get PR metadata and diff
                pr_data = await self._get_pr_data(tools, owner, repo, pr_number)
                diff_content = await self._get_pr_diff(tools, owner, repo, pr_number)
                file_contents = await self._get_changed_files_content(tools, owner, repo, pr_number, pr_data)
                
                # Perform analysis
                analysis = await self._analyze_with_llm(pr_data, diff_content, file_contents)
                
                # Generate review comment
                review_comment = await self._generate_review_comment(analysis)
                
                return self._parse_analysis(analysis, review_comment)

    async def _get_pr_data(self, tools: List, owner: str, repo: str, pr_number: int) -> Dict:
        """Get PR metadata using GitHub MCP tools"""
        try:
            # Find the appropriate MCP tool for getting PR data
            get_pr_tool = next((tool for tool in tools if 'pull' in tool.name.lower() or 'pr' in tool.name.lower()), None)
            
            if get_pr_tool:
                pr_data = await get_pr_tool.ainvoke({
                    "owner": owner,
                    "repo": repo,
                    "pull_number": pr_number
                })
                return pr_data
            else:
                # Fallback: construct basic PR info
                return {
                    "owner": owner,
                    "repo": repo,
                    "number": pr_number,
                    "title": f"PR #{pr_number}",
                    "body": "Unable to fetch PR description"
                }
        except Exception as e:
            print(f"Error fetching PR data: {e}")
            return {"error": str(e)}

    async def _get_pr_diff(self, tools: List, owner: str, repo: str, pr_number: int) -> str:
        """Get PR diff using GitHub MCP tools"""
        try:
            # Find diff/comparison tool
            diff_tool = next((tool for tool in tools if 'diff' in tool.name.lower() or 'compare' in tool.name.lower()), None)
            
            if diff_tool:
                diff_data = await diff_tool.ainvoke({
                    "owner": owner,
                    "repo": repo,
                    "pull_number": pr_number
                })
                return str(diff_data)
            else:
                return "Unable to fetch PR diff"
        except Exception as e:
            print(f"Error fetching PR diff: {e}")
            return f"Error fetching diff: {e}"

    async def _get_changed_files_content(self, tools: List, owner: str, repo: str, pr_number: int, pr_data: Dict) -> Dict:
        """Get content of changed files using GitHub MCP tools"""
        try:
            file_contents = {}
            
            # Find file content tool
            content_tool = next((tool for tool in tools if 'content' in tool.name.lower() or 'file' in tool.name.lower()), None)
            
            if content_tool and 'files' in pr_data:
                for file_info in pr_data.get('files', [])[:5]:  # Limit to first 5 files
                    try:
                        content = await content_tool.ainvoke({
                            "owner": owner,
                            "repo": repo,
                            "path": file_info.get('filename', ''),
                            "ref": "HEAD"
                        })
                        file_contents[file_info.get('filename', '')] = content
                    except Exception as file_error:
                        file_contents[file_info.get('filename', '')] = f"Error fetching content: {file_error}"
            
            return file_contents
        except Exception as e:
            print(f"Error fetching file contents: {e}")
            return {"error": str(e)}

    async def _analyze_with_llm(self, pr_data: Dict, diff_content: str, file_contents: Dict) -> str:
        """Analyze PR data using LLM"""
        try:
            # Format the data for analysis
            pr_info = f"""
Title: {pr_data.get('title', 'N/A')}
Description: {pr_data.get('body', 'N/A')}
Author: {pr_data.get('user', {}).get('login', 'N/A')}
Files Changed: {len(file_contents)}
"""
            
            # Create the analysis chain
            messages = [
                self.system_prompt.format(),
                HumanMessage(content=self.analysis_prompt.format(
                    pr_data=pr_info,
                    diff_content=diff_content[:3000],  # Truncate for token limits
                    file_contents=str(file_contents)[:2000]  # Truncate for token limits
                ))
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            return f"Analysis error: {e}"

    async def _generate_review_comment(self, analysis: str) -> str:
        """Generate a review comment based on analysis"""
        try:
            comment_chain = self.comment_prompt | self.llm
            comment = await comment_chain.ainvoke({"analysis": analysis})
            
            if hasattr(comment, 'content'):
                return comment.content
            return str(comment)
            
        except Exception as e:
            print(f"Error generating comment: {e}")
            return f"Error generating comment: {e}"

    def _parse_analysis(self, analysis: str, review_comment: str) -> PRAnalysis:
        """Parse the LLM analysis into structured format"""
        try:
            # Simple parsing - in production you might want more sophisticated parsing
            lines = analysis.split('\n')
            
            summary = "Analysis completed"
            best_practices = []
            potential_issues = []
            security_concerns = []
            performance_insights = []
            recommendations = []
            code_quality_score = 7  # Default score
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if 'summary' in line.lower():
                    current_section = 'summary'
                elif 'best practices' in line.lower() or 'good' in line.lower():
                    current_section = 'best_practices'
                elif 'issues' in line.lower() or 'problems' in line.lower():
                    current_section = 'issues'
                elif 'security' in line.lower():
                    current_section = 'security'
                elif 'performance' in line.lower():
                    current_section = 'performance'
                elif 'recommendations' in line.lower():
                    current_section = 'recommendations'
                elif 'quality score' in line.lower() or 'score' in line.lower():
                    # Extract numeric score
                    import re
                    score_match = re.search(r'(\d+)', line)
                    if score_match:
                        code_quality_score = int(score_match.group(1))
                elif line.startswith('-') or line.startswith('*'):
                    # This is a list item
                    item = line[1:].strip()
                    if current_section == 'best_practices':
                        best_practices.append(item)
                    elif current_section == 'issues':
                        potential_issues.append(item)
                    elif current_section == 'security':
                        security_concerns.append(item)
                    elif current_section == 'performance':
                        performance_insights.append(item)
                    elif current_section == 'recommendations':
                        recommendations.append(item)
                elif current_section == 'summary':
                    summary = line
            
            return PRAnalysis(
                summary=summary,
                best_practices=best_practices,
                potential_issues=potential_issues,
                security_concerns=security_concerns,
                performance_insights=performance_insights,
                code_quality_score=code_quality_score,
                recommendations=recommendations,
                review_comment=review_comment
            )
            
        except Exception as e:
            print(f"Error parsing analysis: {e}")
            return PRAnalysis(
                summary="Error parsing analysis",
                best_practices=[],
                potential_issues=[f"Parsing error: {e}"],
                security_concerns=[],
                performance_insights=[],
                code_quality_score=5,
                recommendations=[],
                review_comment=review_comment
            )

    def format_analysis_report(self, analysis: PRAnalysis) -> str:
        """Format analysis as a readable report"""
        report = f"""
# PR Review Analysis Report

## Summary
{analysis.summary}

## Code Quality Score: {analysis.code_quality_score}/10

## ✅ Best Practices
"""
        for practice in analysis.best_practices:
            report += f"- {practice}\n"
        
        report += "\n## ⚠️ Potential Issues\n"
        for issue in analysis.potential_issues:
            report += f"- {issue}\n"
            
        if analysis.security_concerns:
            report += "\n## 🔒 Security Concerns\n"
            for concern in analysis.security_concerns:
                report += f"- {concern}\n"
                
        if analysis.performance_insights:
            report += "\n## ⚡ Performance Insights\n"
            for insight in analysis.performance_insights:
                report += f"- {insight}\n"
        
        report += "\n## 💡 Recommendations\n"
        for rec in analysis.recommendations:
            report += f"- {rec}\n"
            
        return report
