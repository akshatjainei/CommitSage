"""
Demo script for PR Review Agent
This script demonstrates how to use the PR Review Agent to analyze a pull request
"""
import os
import asyncio
from dotenv import load_dotenv
from Utils.pr_review_agent import PRReviewAgent

# Load environment variables
load_dotenv()

async def demo_pr_analysis():
    """
    Demo function showing how to analyze a PR
    """
    print("🎯 PR Review Agent Demo")
    print("=" * 40)
    
    # Get API keys
    openai_api_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN", "")
    
    if not openai_api_key:
        print("❌ OPENAI_API_KEY not found. Please set it in .env file")
        return
    
    # Initialize agent
    agent = PRReviewAgent(openai_api_key=openai_api_key, github_token=github_token)
    
    # Example PR to analyze (you can change this)
    owner = "octocat"
    repo = "Hello-World"
    pr_number = 1
    
    print(f"�� Analyzing PR #{pr_number} in {owner}/{repo}")
    print("This is a demo - the PR may not exist, but it shows the workflow")
    
    try:
        # Analyze the PR
        analysis = await agent.analyze_pr(owner, repo, pr_number)
        
        # Display results
        print("\n" + "="*50)
        print("📊 ANALYSIS RESULTS")
        print("="*50)
        
        report = agent.format_analysis_report(analysis)
        print(report)
        
        print("\n" + "="*50)
        print("💬 REVIEW COMMENT")
        print("="*50)
        print(analysis.review_comment)
        
    except Exception as e:
        print(f"❌ Demo error (expected for non-existent PR): {e}")
        print("\n💡 To use with real PRs:")
        print("1. Set your GITHUB_TOKEN in .env")
        print("2. Use a real repository and PR number")
        print("3. Run the main script: python pr_review_main.py")

def create_example_env_file():
    """Create an example .env file"""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# PR Review Agent Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("GITHUB_TOKEN=your_github_token_here\n")
        print("✅ Created .env file template")
    else:
        print("📁 .env file already exists")

if __name__ == "__main__":
    print("🚀 Starting PR Review Agent Demo")
    create_example_env_file()
    asyncio.run(demo_pr_analysis())
