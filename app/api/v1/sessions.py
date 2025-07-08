from fastapi import APIRouter, status, Depends
from app.models.pydantic_schemas import SessionModel, CreateSessionRequest
from fastapi.responses import JSONResponse
from app.services.session_service import SessionService
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
session_service = SessionService()


@router.get("/", response_model=list[SessionModel])
async def list_sessions(db: AsyncSession = Depends(get_db)):
    sessions = await session_service.list_sessions(db)
    return sessions


@router.post("/", response_model=SessionModel, status_code=status.HTTP_201_CREATED)
async def create_session(
    request: CreateSessionRequest, db: AsyncSession = Depends(get_db)
):
    session = await session_service.create_session(db, request.title, request.status)
    return session


@router.get("/{id}/", response_model=SessionModel)
async def get_session(id: int, db: AsyncSession = Depends(get_db)):
    session = await session_service.get_session(db, id)
    if not session:
        return JSONResponse(content={"detail": "Session not found"}, status_code=404)
    return session


@router.put("/{id}/", response_model=SessionModel)
async def update_session(
    id: int, request: CreateSessionRequest, db: AsyncSession = Depends(get_db)
):
    session = await session_service.update_session(db, id, request.dict())
    return session


@router.patch("/{id}/", response_model=SessionModel)
async def patch_session(
    id: int, request: CreateSessionRequest, db: AsyncSession = Depends(get_db)
):
    session = await session_service.update_session(
        db, id, request.dict(exclude_unset=True)
    )
    return session


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(id: int, db: AsyncSession = Depends(get_db)):
    deleted = await session_service.delete_session(db, id)
    if not deleted:
        return JSONResponse(content={"detail": "Session not found"}, status_code=404)
    return JSONResponse(content=None, status_code=204)
