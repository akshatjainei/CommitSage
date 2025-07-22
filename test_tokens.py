#!/usr/bin/env python3
"""
Quick test script to verify GitHub and OpenAI tokens
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_github_token():
    """Test GitHub token"""
    token = os.getenv("GITHUB_TOKEN")
    
    if not token or token == "your_github_token_here":
        print("❌ GitHub token not set in .env file")
        return False
    
    headers = {"Authorization": f"token {token}"}
    
    try:
        # Test with GitHub API - get user info
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub token valid - User: {user_data.get('login')}")
            print(f"   Scopes: {response.headers.get('X-OAuth-Scopes', 'Unknown')}")
            return True
        else:
            print(f"❌ GitHub token invalid - Status: {response.status_code}")
            print(f"   Error: {response.json().get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing GitHub token: {e}")
        return False

def test_openai_key():
    """Test OpenAI API key"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ OpenAI API key not set in .env file")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test with a simple API call
        response = requests.get("https://api.openai.com/v1/models", headers=headers)
        
        if response.status_code == 200:
            print("✅ OpenAI API key valid")
            return True
        else:
            print(f"❌ OpenAI API key invalid - Status: {response.status_code}")
            print(f"   Error: {response.json().get('error', {}).get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing OpenAI key: {e}")
        return False

def main():
    print("🧪 Testing API Tokens")
    print("=" * 25)
    
    github_ok = test_github_token()
    print()
    openai_ok = test_openai_key()
    
    print("\n" + "=" * 25)
    if github_ok and openai_ok:
        print("🎉 All tokens are valid! You're ready to use the PR Review Agent.")
        print("Run: python3 pr_review_main.py")
    else:
        print("⚠️  Please fix the token issues above before proceeding.")
        print("\n💡 Token Setup Instructions:")
        print("1. GitHub: https://github.com/settings/tokens")
        print("2. OpenAI: https://platform.openai.com/api-keys")
        print("3. Edit .env file with your actual tokens")

if __name__ == "__main__":
    main()
