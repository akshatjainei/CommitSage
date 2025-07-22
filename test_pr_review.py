"""
Test script for PR Review Agent
This script performs basic validation of the PR Review Agent setup
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import asyncio
        print("✅ asyncio imported")
    except ImportError as e:
        print(f"❌ asyncio import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain-openai imported")
    except ImportError as e:
        print(f"❌ langchain-openai import failed: {e}")
        return False
    
    try:
        from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate
        print("✅ langchain prompts imported")
    except ImportError as e:
        print(f"❌ langchain prompts import failed: {e}")
        return False
    
    try:
        from Utils.pr_review_agent import PRReviewAgent, PRAnalysis
        print("✅ PR Review Agent imported")
    except ImportError as e:
        print(f"❌ PR Review Agent import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🌍 Testing environment...")
    
    if not os.path.exists(".env"):
        print("⚠️  .env file not found")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("⚠️  OPENAI_API_KEY not set in .env")
        return False
    else:
        print("✅ OPENAI_API_KEY found")
    
    if not github_token or github_token == "your_github_token_here":
        print("⚠️  GITHUB_TOKEN not set in .env (optional)")
    else:
        print("✅ GITHUB_TOKEN found")
    
    return True

def test_agent_initialization():
    """Test PR Review Agent initialization"""
    print("\n🤖 Testing agent initialization...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv("OPENAI_API_KEY")
        github_token = os.getenv("GITHUB_TOKEN", "")
        
        if not openai_key or openai_key == "your_openai_api_key_here":
            print("⚠️  Cannot test agent initialization without valid OPENAI_API_KEY")
            return False
        
        from Utils.pr_review_agent import PRReviewAgent
        agent = PRReviewAgent(openai_api_key=openai_key, github_token=github_token)
        print("✅ PR Review Agent initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 PR Review Agent Test Suite")
    print("=" * 35)
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment),
        ("Agent Initialization Test", test_agent_initialization)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 35)
    print("📊 Test Results")
    print("=" * 35)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your PR Review Agent is ready to use.")
        print("Run: python pr_review_main.py")
    else:
        print("\n⚠️  Some tests failed. Please check the setup:")
        print("1. Run: python setup_pr_review.py")
        print("2. Configure your .env file")
        print("3. Install missing dependencies")

if __name__ == "__main__":
    main()
