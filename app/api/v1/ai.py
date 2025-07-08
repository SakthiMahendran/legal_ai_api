from fastapi import APIRouter, status, Depends
from app.models.pydantic_schemas import (
    GenerateRequest,
    GenerateResponse,
    RefineRequest,
    ExtractDetailsRequest,
    ExtractDetailsResponse,
    AIHealthResponse,
    MessageModel,
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from pydantic import BaseModel
from typing import List

router = APIRouter()

from app.services.drafting_service import DraftingService
from app.services.message_service import MessageService

drafting_service = DraftingService()
message_service = MessageService()


# Chat models
class ChatRequest(BaseModel):
    session_id: int
    message: str


class ChatResponse(BaseModel):
    user_message: MessageModel
    ai_message: MessageModel


@router.post("/chat/", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Send a message to AI and get a response. Saves both messages to the session.
    """
    try:
        # Save user message
        user_message = await message_service.create_message(
            db=db, session_id=request.session_id, role="user", content=request.message
        )

        if not user_message:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Session not found")

        # Get conversation history for context
        messages = await message_service.list_messages(
            db, session_id=request.session_id
        )
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages[-10:]  # Last 10 messages
        ]

        # Generate AI response
        ai_response = drafting_service.generate_document(
            prompt=request.message, conversation_history=conversation_history
        )

        # If AI response is empty, provide a helpful fallback
        if not ai_response or ai_response.strip() == "":
            ai_response = f"""I understand you're asking about: "{request.message}"

I'm here to help with legal document drafting and legal questions. Here are some things I can help you with:

1. **Document Generation**: I can draft NDAs, contracts, lease agreements, and other legal documents
2. **Legal Questions**: I can provide general information about legal concepts
3. **Document Review**: I can help explain legal terms and clauses

Could you please provide more specific details about what type of legal document or information you need?

[Note: This is general information only and not legal advice. Please consult with a qualified attorney for specific legal matters.]"""

        # Save AI response
        ai_message = await message_service.create_message(
            db=db, session_id=request.session_id, role="assistant", content=ai_response
        )

        # Refresh objects to ensure all attributes are loaded
        await db.refresh(user_message)
        await db.refresh(ai_message)

        # Convert SQLAlchemy objects to Pydantic models explicitly
        user_msg_dict = {
            "id": user_message.id,
            "session_id": user_message.session_id,
            "role": user_message.role,
            "content": user_message.content,
            "created_at": user_message.created_at,
        }

        ai_msg_dict = {
            "id": ai_message.id,
            "session_id": ai_message.session_id,
            "role": ai_message.role,
            "content": ai_message.content,
            "created_at": ai_message.created_at,
        }

        return ChatResponse(
            user_message=MessageModel(**user_msg_dict),
            ai_message=MessageModel(**ai_msg_dict),
        )

    except Exception as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.post("/generate/", response_model=GenerateResponse)
def generate_document(request: GenerateRequest):
    """
    Generate a legal document using the DraftingService (LLM agent).
    """
    try:
        result = drafting_service.generate_document(
            prompt=request.prompt, conversation_history=request.conversation_history
        )

        # If result is empty or contains error, provide fallback
        if not result or result.strip() == "" or "Error:" in result:
            result = generate_fallback_document(request.prompt)

        return GenerateResponse(result=result)
    except Exception as e:
        # Fallback to template-based generation
        fallback_result = generate_fallback_document(request.prompt)
        return GenerateResponse(
            result=f"{fallback_result}\n\n[Note: Generated using fallback template due to AI service unavailability]"
        )


@router.post("/refine/", response_model=GenerateResponse)
def refine_document(request: RefineRequest):
    """
    Refine a legal document draft using the DraftingService (LLM agent).
    """
    result = drafting_service.refine_document(
        current_draft=request.current_draft, user_request=request.user_request
    )
    return GenerateResponse(result=result)


@router.post("/extract-details/", response_model=ExtractDetailsResponse)
def extract_details(request: ExtractDetailsRequest):
    """
    Extract structured details from conversation history using the DraftingService.
    """
    details = drafting_service.extract_details(request.conversation_history)
    return ExtractDetailsResponse(**details)


@router.get("/health/", response_model=AIHealthResponse)
def ai_health():
    # TODO: Implement AI health check
    return JSONResponse(content={"detail": "Not implemented"}, status_code=501)
