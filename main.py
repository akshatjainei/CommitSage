import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate
from langchain.agents import AgentExecutor, Tool
from Utils.git_util import get_git_root, get_staged_diff
from Utils.diff_parser import parse_diff

def format_commit_message(message) -> str:
    if hasattr(message, "content"):
        message = message.content
    message = message.strip()
    if not message.lower().startswith("commit message:"):
        message = f"Commit Message: {message}"
    return message

prompt_template = PromptTemplate(
    input_variables=["diff_summary"],
    template="""
You are an expert at writing concise and descriptive git commit messages.
Given the following code changes, generate a commit message that summarizes the intent:

{diff_summary}
"""
)

def build_commit_message_chain():
    llm = ChatOpenAI(temperature=0.2, model="gpt-4o-mini")
    return prompt_template | llm | format_commit_message

load_dotenv()

def main():
    print("🚀 CommitSage - AI-Powered Git Tools")
    print("=" * 40)
    print("1. Generate Commit Message")
    print("2. PR Review Agent")
    print("3. Exit")
    
    choice = input("\nSelect an option (1-3): ").strip()
    
    if choice == "1":
        generate_commit_message()
    elif choice == "2":
        run_pr_review_agent()
    elif choice == "3":
        print("👋 Goodbye!")
        return
    else:
        print("❌ Invalid choice. Please select 1, 2, or 3.")
        main()

def generate_commit_message():
    """Generate commit message functionality"""
    repo_path = input("Enter the path to the git repository (or '.' for current directory): ").strip()
    # Get git root
    git_root = get_git_root(repo_path)
    # Get staged diff
    diff = get_staged_diff(git_root)
    # Parse diff
    diff_summary = parse_diff(diff)
    # Format summary for LLM
    summary_str = ""
    for fname, changes in diff_summary.items():
        summary_str += f"File: {fname}\n"
        for change in changes:
            summary_str += f"  {change}\n"
    commit_message_chain = build_commit_message_chain()
    commit_message = commit_message_chain.invoke({"diff_summary": summary_str})
    print("\nSuggested commit message:")
    print(commit_message)

def run_pr_review_agent():
    """Run the PR Review Agent"""
    print("\n🔍 Starting PR Review Agent...")
    print("Please run: python pr_review_main.py")
    print("Or check the README_PR_Review.md for detailed instructions.")

if __name__ == "__main__":
    main()