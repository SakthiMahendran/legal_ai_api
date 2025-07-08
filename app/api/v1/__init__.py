from fastapi import APIRouter
from .auth import router as auth_router
from .sessions import router as sessions_router
from .messages import router as messages_router
from .ai import router as ai_router
from .documents import router as documents_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(sessions_router, prefix="/sessions", tags=["sessions"])
router.include_router(messages_router, prefix="/messages", tags=["messages"])
router.include_router(ai_router, prefix="/ai", tags=["ai"])
router.include_router(documents_router, prefix="/documents", tags=["documents"])
