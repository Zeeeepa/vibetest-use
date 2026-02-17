#!/usr/bin/env python3
"""
Test script to verify Google API key works with Gemini
Run this to test your API key before using the DXT
"""
import os
import sys

def test_api_key():
    """Test if the Google API key works"""
    print("🔍 Testing Google API Key for Vibetest DXT...")
    
    # Check for API key
    api_key = None
    for env_var in ["GOOGLE_API_KEY", "GEMINI_API_KEY", "GOOGLE_GENAI_API_KEY"]:
        api_key = os.getenv(env_var)
        if api_key and api_key.strip():
            print(f"✅ Found API key in {env_var}")
            api_key = api_key.strip()
            break
    
    if not api_key:
        print("❌ No API key found!")
        print("📋 Please set one of these environment variables:")
        print("   - GOOGLE_API_KEY")
        print("   - GEMINI_API_KEY") 
        print("   - GOOGLE_GENAI_API_KEY")
        print("🔗 Get your API key from: https://aistudio.google.com/app/apikey")
        return False
    
    # Test the API key
    try:
        print("🧪 Testing API key with Gemini...")
        
        # Try to import required packages
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.messages import HumanMessage
        except ImportError as e:
            print(f"❌ Missing required packages: {e}")
            print("📦 Install with: pip install langchain_google_genai langchain_core")
            return False
        
        # Test API call
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_key,
            temperature=0.1
        )
        
        response = llm.invoke([HumanMessage(content="Hello! Just testing the API connection. Please respond with 'API test successful'.")])
        
        if "successful" in response.content.lower():
            print("✅ API key test successful!")
            print("🎉 Your Vibetest DXT should work properly")
            return True
        else:
            print("⚠️  API responded but with unexpected content:")
            print(f"   Response: {response.content}")
            return False
            
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        print("🔧 Possible issues:")
        print("   - Invalid API key")
        print("   - Billing not enabled in Google Cloud")
        print("   - API quotas exceeded")
        print("   - Network connectivity issues")
        return False

if __name__ == "__main__":
    print("🚀 Vibetest DXT API Key Test")
    print("=" * 40)
    
    success = test_api_key()
    
    print("\n" + "=" * 40)
    if success:
        print("🎯 Ready to use Vibetest DXT!")
        sys.exit(0)
    else:
        print("🔧 Please fix the issues above before using the DXT")
        sys.exit(1)
