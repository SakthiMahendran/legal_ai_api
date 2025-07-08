#!/usr/bin/env python3

import sys
sys.path.append('.')
import os
from drafting.graph import LegalDocumentAgent
from drafting.prompt_templates import DOCUMENT_GENERATION_PROMPT

def debug_llm():
    print('=== Debugging LLM Call ===')
    print(f'OPENROUTER_API_KEY present: {bool(os.getenv("OPENROUTER_API_KEY"))}')
    
    try:
        agent = LegalDocumentAgent()
        print('✅ LegalDocumentAgent initialized successfully')
        print(f'Model: {agent.model}')
        print(f'Base URL: {agent.llm_client.base_url}')
        
        # Test simple LLM call first
        print('\n=== Testing Simple LLM Call ===')
        simple_prompt = "Say hello and confirm you are working."
        simple_input = {}
        
        simple_result = agent.get_llm_response(simple_prompt, simple_input)
        print(f'Simple result: "{simple_result}"')
        print(f'Simple result length: {len(simple_result)}')
        print(f'Starts with error: {simple_result.lower().startswith("error") if simple_result else "N/A"}')
        
        # Test document generation prompt
        print('\n=== Testing Document Generation Prompt ===')
        test_input = {
            "document_type": "nda",
            "collected_info": "Disclosing Party: ABC Corp\nReceiving Party: XYZ Inc\nPurpose: Business discussions",
            "date": "January 1, 2025"
        }
        
        doc_result = agent.get_llm_response(DOCUMENT_GENERATION_PROMPT, test_input)
        print(f'Document result: "{doc_result[:200]}..."' if len(doc_result) > 200 else f'Document result: "{doc_result}"')
        print(f'Document result length: {len(doc_result)}')
        print(f'Starts with error: {doc_result.lower().startswith("error") if doc_result else "N/A"}')
        
        # Test the condition logic
        print('\n=== Testing Condition Logic ===')
        condition1 = doc_result and not doc_result.lower().startswith("error")
        print(f'doc_result exists: {bool(doc_result)}')
        print(f'doc_result.lower().startswith("error"): {doc_result.lower().startswith("error") if doc_result else "N/A"}')
        print(f'Final condition (should be True for success): {condition1}')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_llm()
