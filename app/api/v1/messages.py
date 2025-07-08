from fastapi import APIRouter, Query, status, Depends
from app.models.pydantic_schemas import MessageModel, CreateMessageRequest
from fastapi.responses import JSONResponse
from app.services.message_service import MessageService
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
message_service = MessageService()


@router.get("/", response_model=list[MessageModel])
async def list_messages(
    session_id: int = Query(None, description="Filter by session ID"),
    db: AsyncSession = Depends(get_db),
):
    messages = await message_service.list_messages(db, session_id=session_id)
    return messages


@router.post("/", response_model=MessageModel, status_code=status.HTTP_201_CREATED)
async def create_message(
    request: CreateMessageRequest, db: AsyncSession = Depends(get_db)
):
    msg = await message_service.create_message(
        db=db, session_id=request.session_id, role=request.role, content=request.content
    )
    if not msg:
        return JSONResponse(content={"detail": "Session not found"}, status_code=404)
    return msg
