"""
Setup script for PR Review Agent
This script helps set up the environment and dependencies for the PR Review Agent
"""
import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
    return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    try:
        with open(".env", "w") as f:
            f.write("# PR Review Agent Configuration\n")
            f.write("# Get your OpenAI API key from: https://platform.openai.com/api-keys\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# Get your GitHub token from: https://github.com/settings/tokens\n")
            f.write("# Required permissions: repo, read:org, read:user\n")
            f.write("GITHUB_TOKEN=your_github_token_here\n")
        
        print("✅ .env file created")
        print("📋 Please edit .env and add your API keys")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def verify_mcp_server():
    """Verify GitHub MCP Server can be installed"""
    print("🔧 Verifying GitHub MCP Server availability...")
    try:
        # Test if npx can find the GitHub MCP server
        result = subprocess.run(
            ["npx", "--yes", "@modelcontextprotocol/server-github", "--help"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print("✅ GitHub MCP Server is available")
            return True
        else:
            print("⚠️  GitHub MCP Server test failed, but may work during runtime")
            return True
    except subprocess.TimeoutExpired:
        print("⚠️  GitHub MCP Server test timed out, but may work during runtime")
        return True
    except FileNotFoundError:
        print("❌ npx not found. Please ensure Node.js is properly installed")
        return False
    except Exception as e:
        print(f"⚠️  Could not verify GitHub MCP Server: {e}")
        return True

def main():
    """Main setup function"""
    print("🚀 PR Review Agent Setup")
    print("=" * 30)
    
    # Check requirements
    checks = [
        check_python_version(),
        check_node_installed(),
        install_dependencies(),
        create_env_file(),
        verify_mcp_server()
    ]
    
    if all(checks):
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit .env file and add your API keys")
        print("2. Run: python demo_pr_review.py (for demo)")
        print("3. Run: python pr_review_main.py (for interactive use)")
        print("4. Check README_PR_Review.md for detailed documentation")
    else:
        print("\n❌ Setup incomplete. Please resolve the issues above.")

if __name__ == "__main__":
    main()
