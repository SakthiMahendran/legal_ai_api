#!/usr/bin/env python3

import sys
sys.path.append('.')
from app.services.drafting_service import DraftingService
import os

def test_ai_service():
    print('Testing DraftingService...')
    print(f'OPENROUTER_API_KEY present: {bool(os.getenv("OPENROUTER_API_KEY"))}')
    
    try:
        service = DraftingService()
        print('DraftingService initialized successfully')
        
        # Test document generation
        result = service.generate_document(
            prompt='Draft a simple NDA agreement.',
            conversation_history=[]
        )
        print(f'Generated result: "{result}"')
        print(f'Result length: {len(result)}')
        
        if not result or result.strip() == "":
            print('WARNING: Empty result returned!')
        
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_service()
