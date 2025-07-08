from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.models.sql_models import Document as DocumentModel
from sqlalchemy import update
from datetime import datetime


class DocumentService:
    async def create_document(
        self,
        db: AsyncSession,
        session_id: int,
        title: str,
        filename: str,
        file_path: str,
        status: str = "active",
    ):
        document = DocumentModel(
            session_id=session_id,
            title=title,
            filename=filename,
            file_path=file_path,
            status=status,
        )
        db.add(document)
        await db.commit()
        await db.refresh(document)
        return document

    async def list_documents(self, db: AsyncSession, session_id: int = None):
        if session_id:
            result = await db.execute(
                select(DocumentModel).where(DocumentModel.session_id == session_id)
            )
        else:
            result = await db.execute(select(DocumentModel))
        return result.scalars().all()

    async def get_document(self, db: AsyncSession, document_id: int):
        result = await db.execute(
            select(DocumentModel).where(DocumentModel.id == document_id)
        )
        return result.scalar_one_or_none()

    async def update_document(self, db: AsyncSession, document_id: int, updates: dict):
        await db.execute(
            update(DocumentModel)
            .where(DocumentModel.id == document_id)
            .values(**updates, updated_at=datetime.utcnow())
        )
        await db.commit()
        return await self.get_document(db, document_id)

    async def delete_document(self, db: AsyncSession, document_id: int):
        document = await self.get_document(db, document_id)
        if document:
            await db.delete(document)
            await db.commit()
            return True
        return False
