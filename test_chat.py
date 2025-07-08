#!/usr/bin/env python3

import asyncio
import sys
sys.path.append('.')

from app.api.v1.ai import chat_with_ai, ChatRequest
from app.db import AsyncSessionLocal
from app.services.session_service import SessionService

async def test_chat():
    print('=== Testing AI Chat Endpoint ===')
    
    # Create a test session first
    session_service = SessionService()
    async with AsyncSessionLocal() as db:
        session = await session_service.create_session(db, 'Test Chat Session', 'active')
        print(f'Created session: {session.id}')
        
        # Test chat request
        chat_request = ChatRequest(
            session_id=session.id,
            message="What is a contract and what are its key elements?"
        )
        
        try:
            response = await chat_with_ai(chat_request, db)
            print(f'Chat response type: {type(response)}')
            print(f'User message: {response.user_message.content}')
            print(f'AI message length: {len(response.ai_message.content)}')
            print(f'AI message preview: {response.ai_message.content[:200]}...')
        except Exception as e:
            print(f'Error: {e}')
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat())
