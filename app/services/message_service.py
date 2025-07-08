from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from legal_ai_api.app.models.sql_models import Message as MessageModel
from sqlalchemy import update
from datetime import datetime

class MessageService:
    async def create_message(self, db: AsyncSession, session_id: int, role: str, content: str, metadata: dict = None):
        message = MessageModel(session_id=session_id, role=role, content=content)
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    async def list_messages(self, db: AsyncSession, session_id: int = None):
        if session_id:
            result = await db.execute(select(MessageModel).where(MessageModel.session_id == session_id))
        else:
            result = await db.execute(select(MessageModel))
        return result.scalars().all()

    async def get_message(self, db: AsyncSession, message_id: int):
        result = await db.execute(select(MessageModel).where(MessageModel.id == message_id))
        return result.scalar_one_or_none()

    async def update_message(self, db: AsyncSession, message_id: int, updates: dict):
        await db.execute(update(MessageModel).where(MessageModel.id == message_id).values(**updates, updated_at=datetime.utcnow()))
        await db.commit()
        return await self.get_message(db, message_id)

    async def delete_message(self, db: AsyncSession, message_id: int):
        message = await self.get_message(db, message_id)
        if message:
            await db.delete(message)
            await db.commit()
            return True
        return False
