#!/usr/bin/env python3

import sys
sys.path.append('.')
import os
from drafting.graph import LegalDocumentAgent

def test_llm_direct():
    print('Testing LegalDocumentAgent directly...')
    print(f'OPENROUTER_API_KEY: {os.getenv("OPENROUTER_API_KEY")[:10]}...' if os.getenv("OPENROUTER_API_KEY") else 'Not set')
    
    try:
        agent = LegalDocumentAgent()
        print('LegalDocumentAgent initialized successfully')
        
        # Test LLM response directly
        test_prompt = "Generate a simple greeting message."
        test_input = {"message": "Hello"}
        
        print(f'Testing LLM with prompt: "{test_prompt}"')
        result = agent.get_llm_response(test_prompt, test_input)
        print(f'LLM result: "{result}"')
        print(f'Result length: {len(result)}')
        
        # Test document generation workflow
        print('\nTesting document generation workflow...')
        from drafting.graph import AgentState
        
        state = {
            "session_id": "test-session",
            "user_input": "Draft a simple NDA agreement.",
            "document_type": "",
            "collected_info": {},
            "current_question": "",
            "conversation_history": [],
            "is_complete": False,
            "final_document": "",
            "error_message": "",
        }
        
        # Test identify document type
        state = agent.identify_document_type(state)
        print(f'Document type identified: {state.get("document_type")}')
        
        # Test generate document
        state["is_complete"] = True  # Skip Q&A for testing
        state = agent.generate_document(state)
        print(f'Final document: "{state.get("final_document", "")}"')
        
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_direct()
