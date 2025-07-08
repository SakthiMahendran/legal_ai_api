import os
from legal_ai_api.document_qa.graphRag import DocumentQARAG

class DocumentQAService:
    """
    Service wrapper for DocumentQARAG (RAG agent) for FastAPI integration.
    """
    def __init__(self):
        self.rag_agent = DocumentQARAG()

    def answer_query(self, query: str, session_id: str = None) -> dict:
        # Use the RAG agent to answer a query over uploaded documents
        return self.rag_agent.query_documents(query, session_id=session_id)

    def upload_document(self, file_bytes: bytes, filename: str, session_id: str = None) -> dict:
        # Use the RAG agent to upload and index a document
        return self.rag_agent.upload_document(file_bytes, filename, session_id=session_id)

    def list_documents(self, session_id: str = None) -> list:
        # List documents for a session
        return self.rag_agent.list_documents(session_id=session_id)

    def health_check(self) -> dict:
        return {
            "status": "healthy",
            "ai_configured": bool(self.rag_agent),
            "modules_loaded": True,
            "debug_mode": False
        }
