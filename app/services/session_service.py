from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.models.sql_models import Session as SessionModel
from app.models.sql_models import User as UserModel
from sqlalchemy import update
from datetime import datetime


class SessionService:
    async def create_session(
        self, db: AsyncSession, title: str, status: str = "active", user_id: int = None
    ):
        session = SessionModel(title=title, status=status, user_id=user_id)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    async def get_session(self, db: AsyncSession, session_id: int):
        result = await db.execute(
            select(SessionModel).where(SessionModel.id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_sessions(self, db: AsyncSession, user_id: int = None):
        if user_id:
            result = await db.execute(
                select(SessionModel).where(SessionModel.user_id == user_id)
            )
        else:
            result = await db.execute(select(SessionModel))
        return result.scalars().all()

    async def update_session(self, db: AsyncSession, session_id: int, updates: dict):
        await db.execute(
            update(SessionModel)
            .where(SessionModel.id == session_id)
            .values(**updates, updated_at=datetime.utcnow())
        )
        await db.commit()
        return await self.get_session(db, session_id)

    async def delete_session(self, db: AsyncSession, session_id: int):
        session = await self.get_session(db, session_id)
        if session:
            await db.delete(session)
            await db.commit()
            return True
        return False
