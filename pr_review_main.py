import os
import asyncio
from dotenv import load_dotenv
from Utils.pr_review_agent import PRReviewAgent

# Load environment variables
load_dotenv()

async def main():
    """
    Main function to run the PR Review Agent
    """
    print("🔍 PR Review Agent - Powered by GitHub MCP Server")
    print("=" * 50)
    
    # Get API keys from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not openai_api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        return
    
    if not github_token:
        print("⚠️  Warning: GITHUB_TOKEN not found in environment variables")
        print("Public repositories will work, but private repos may not be accessible")
        github_token = ""
    
    # Initialize the PR Review Agent
    agent = PRReviewAgent(openai_api_key=openai_api_key, github_token=github_token)
    
    while True:
        print("\n" + "="*50)
        print("Enter PR details (or 'quit' to exit):")
        
        # Get user input
        owner = input("Repository owner: ").strip()
        if owner.lower() == 'quit':
            break
            
        repo = input("Repository name: ").strip()
        if repo.lower() == 'quit':
            break
            
        try:
            pr_number = int(input("PR number: ").strip())
        except ValueError:
            print("❌ Invalid PR number. Please enter a valid integer.")
            continue
        
        print(f"\n🔄 Analyzing PR #{pr_number} in {owner}/{repo}...")
        print("This may take a few moments...")
        
        try:
            # Analyze the PR
            analysis = await agent.analyze_pr(owner, repo, pr_number)
            
            # Display results
            print("\n" + "="*60)
            print("📊 ANALYSIS COMPLETE")
            print("="*60)
            
            print(agent.format_analysis_report(analysis))
            
            print("\n" + "="*60)
            print("💬 GENERATED REVIEW COMMENT")
            print("="*60)
            print(analysis.review_comment)
            
            # Ask if user wants to save the report
            save_report = input("\n💾 Save analysis report to file? (y/n): ").strip().lower()
            if save_report == 'y':
                filename = f"pr_review_{owner}_{repo}_{pr_number}.md"
                with open(filename, 'w') as f:
                    f.write(agent.format_analysis_report(analysis))
                    f.write("\n\n## Generated Review Comment\n\n")
                    f.write(analysis.review_comment)
                print(f"✅ Report saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error analyzing PR: {e}")
            print("Please check your inputs and try again.")
    
    print("\n👋 Thanks for using PR Review Agent!")

def setup_environment():
    """
    Set up the environment and provide instructions
    """
    env_file = ".env"
    if not os.path.exists(env_file):
        print("🔧 Setting up environment...")
        with open(env_file, 'w') as f:
            f.write("# PR Review Agent Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("GITHUB_TOKEN=your_github_token_here\n")
        
        print(f"✅ Created {env_file}")
        print("\n📝 Please edit the .env file and add your API keys:")
        print("   - OPENAI_API_KEY: Your OpenAI API key")
        print("   - GITHUB_TOKEN: Your GitHub personal access token (optional)")
        print("\n🔗 To get a GitHub token, visit:")
        print("   https://github.com/settings/tokens")
        return False
    return True

if __name__ == "__main__":
    print("🚀 Starting PR Review Agent...")
    
    # Setup environment if needed
    if not setup_environment():
        print("\n⚠️  Please configure your .env file and run the script again.")
    else:
        # Run the main application
        asyncio.run(main())
