#!/usr/bin/env python3

import os
import requests
import json

def test_openrouter_direct():
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"API Key: {api_key[:10]}...{api_key[-10:] if api_key else 'None'}")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    # Test direct HTTP request to OpenRouter
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Legal AI API",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [
            {"role": "user", "content": "Say hello and confirm you are working."}
        ],
        "temperature": 0.3,
        "max_tokens": 100
    }
    
    try:
        print("🔄 Making direct HTTP request to OpenRouter...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ Success! Response: {content}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_openrouter_direct()
