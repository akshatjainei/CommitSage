# PR Review Agent 🔍

A sophisticated PR Review Agent that uses the GitHub MCP (Model Context Protocol) Server to analyze pull requests and provide comprehensive feedback including best practices, potential issues, security concerns, and actionable recommendations.

## Features ✨

- **Comprehensive Code Analysis**: Analyzes code quality, best practices, and potential issues
- **Security Assessment**: Identifies security vulnerabilities and concerns
- **Performance Insights**: Provides performance optimization suggestions
- **GitHub MCP Integration**: Leverages GitHub MCP Server for seamless GitHub API integration
- **AI-Powered Reviews**: Uses OpenAI GPT models for intelligent code analysis
- **Structured Reporting**: Generates detailed analysis reports and review comments
- **Interactive CLI**: User-friendly command-line interface

## What the Agent Analyzes 📊

### Code Quality & Best Practices
- Adherence to coding standards
- Code structure and organization
- Naming conventions
- Documentation completeness

### Potential Issues
- Logic errors and bugs
- Edge case handling
- Error handling patterns
- Code complexity

### Security Concerns
- Vulnerability detection
- Authentication/authorization issues
- Input validation
- Data exposure risks

### Performance Insights
- Optimization opportunities
- Resource usage patterns
- Scalability considerations
- Database query efficiency

## Installation & Setup 🚀

### Prerequisites
- Python 3.8+
- Node.js (for GitHub MCP Server)
- OpenAI API Key
- GitHub Token (optional, for private repositories)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
```

### 3. Install GitHub MCP Server
The agent automatically installs the GitHub MCP Server using npx when needed.

## Usage 🎯

### Interactive Mode
```bash
python pr_review_main.py
```

Follow the prompts to enter:
- Repository owner
- Repository name  
- PR number

### Demo Mode
```bash
python demo_pr_review.py
```

### Programmatic Usage
```python
import asyncio
from Utils.pr_review_agent import PRReviewAgent

async def analyze_pr():
    agent = PRReviewAgent(
        openai_api_key="your_key",
        github_token="your_token"
    )
    
    analysis = await agent.analyze_pr("owner", "repo", 123)
    print(agent.format_analysis_report(analysis))

asyncio.run(analyze_pr())
```

## Configuration ⚙️

### MCP Server Configuration
The agent uses the following MCP configuration (`mcp_config.json`):

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github", "--github-token", "${GITHUB_TOKEN}"]
    }
  }
}
```

### Agent Parameters
- **Model**: GPT-4o-mini (configurable)
- **Temperature**: 0.3 (for consistent analysis)
- **Analysis Depth**: Comprehensive (covers all aspects)

## Output Format 📋

### Analysis Report
```markdown
# PR Review Analysis Report

## Summary
Brief overview of the changes and overall assessment

## Code Quality Score: X/10

## ✅ Best Practices
- Good practices found in the PR

## ⚠️ Potential Issues  
- Issues that need attention

## 🔒 Security Concerns
- Security-related findings

## ⚡ Performance Insights
- Performance optimization opportunities

## 💡 Recommendations
- Specific improvement suggestions
```

### Review Comment
Professional, constructive GitHub-ready review comment with:
- Acknowledgment of good practices
- Clear explanation of issues
- Actionable recommendations
- Collaborative tone

## File Structure 📁

```
CommitSage/
├── main.py                     # Original commit message generator
├── pr_review_main.py          # Main PR review application
├── demo_pr_review.py          # Demo script
├── requirements.txt           # Updated dependencies
├── mcp_config.json           # MCP server configuration
├── .env                      # Environment variables
└── Utils/
    ├── pr_review_agent.py    # Core PR review agent class
    ├── github_mcp_tools.py   # GitHub MCP toolkit
    ├── diff_parser.py        # Existing diff parser
    ├── git_util.py          # Existing git utilities
    └── tools.py             # Existing tools
```

## Error Handling 🛡️

The agent includes comprehensive error handling for:
- Network connectivity issues
- GitHub API rate limits
- Missing permissions
- Invalid repository/PR data
- MCP server communication errors

## Best Practices 💡

### For Repository Owners
- Ensure PR descriptions are comprehensive
- Add appropriate labels and metadata
- Include test cases with PRs

### For Reviewers
- Use the agent as a starting point, not replacement for human review
- Verify security recommendations before implementing
- Consider context that the agent might miss

## Limitations ⚠️

- Token limits may truncate very large PRs
- Analysis quality depends on PR description completeness
- Private repositories require valid GitHub token
- Some GitHub MCP tools may have usage limits

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Troubleshooting 🔧

### Common Issues

**MCP Server Connection Error**
```bash
# Ensure npx is installed
npm install -g npx

# Verify GitHub token permissions
# Token needs: repo, read:org, read:user permissions
```

**Missing Dependencies**
```bash
pip install --upgrade -r requirements.txt
```

**Rate Limiting**
- Use GitHub token for higher rate limits
- Implement delays between requests
- Consider GitHub Enterprise for higher limits

## Security 🔐

- Store API keys securely in `.env` file
- Never commit tokens to version control
- Use minimal required GitHub token permissions
- Regularly rotate API keys

## License 📜

This project is part of the CommitSage suite and follows the same license terms.

## Support 💬

For issues and questions:
1. Check the troubleshooting section
2. Review GitHub MCP Server documentation
3. Create an issue with detailed error information

---

**Happy Reviewing!** 🎉
