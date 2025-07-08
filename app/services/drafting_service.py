import os
from typing import List, Dict, Any
from drafting.graph import LegalDocumentAgent, AgentState
from drafting.memory import SessionMemoryManager


class DraftingMessageService:
    """
    Service to manage chat/message history for drafting sessions.
    Stores messages in session memory using SessionMemoryManager.
    """

    def __init__(self):
        self.manager = SessionMemoryManager()

    def list_messages(self, session_id: str = None):
        # Return all messages for a given session_id, or all if not specified
        if session_id:
            session = self.manager.get_session(session_id)
            return session.get("conversation_history", []) if session else []
        # If no session_id, aggregate all messages from all sessions
        all_msgs = []
        for sid in self.manager.list_sessions():
            session = self.manager.get_session(sid)
            all_msgs.extend(session.get("conversation_history", []))
        return all_msgs

    def create_message(
        self, session_id: str, role: str, content: str, metadata: dict = None
    ):
        session = self.manager.get_session(session_id)
        if not session:
            return None
        msg = {
            "id": f"msg_{len(session.get('conversation_history', []))+1}",
            "session": session_id,
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "created_at": session.get("last_updated"),
        }
        session.setdefault("conversation_history", []).append(msg)
        self.manager.save_session(session_id, session)
        return msg


class DraftingSessionService:
    """
    Service wrapper for SessionMemoryManager to provide session CRUD for FastAPI endpoints.
    """

    def __init__(self):
        self.manager = SessionMemoryManager()

    def list_sessions(self):
        session_ids = self.manager.list_sessions()
        return [self.manager.get_session(sid) for sid in session_ids]

    def create_session(self, title: str, status: str):
        session_id = self.manager.create_session(title, status)
        return self.manager.get_session(session_id)

    def get_session(self, session_id: str):
        return self.manager.get_session(session_id)

    def update_session(self, session_id: str, updates: dict):
        return self.manager.update_session(session_id, updates)

    def patch_session(self, session_id: str, updates: dict):
        return self.manager.update_session(session_id, updates)

    def delete_session(self, session_id: str):
        return self.manager.delete_session(session_id)


class DraftingService:
    """
    Service wrapper for LegalDocumentAgent to integrate with FastAPI endpoints.
    """

    def __init__(self):
        self.agent = LegalDocumentAgent()

    def generate_document(
        self, prompt: str, conversation_history: List[Dict[str, str]]
    ) -> str:
        # Compose initial state from prompt and conversation history
        state = AgentState(
            session_id="api-session",
            user_input=prompt,
            document_type="",
            collected_info={},
            current_question="",
            conversation_history=conversation_history,
            is_complete=False,
            final_document="",
            error_message="",
        )
        state_dict = state.model_dump()
        # Identify document type
        state_dict = self.agent.identify_document_type(state_dict)
        # Collect info via questions if needed (simulate Q&A loop)
        state_dict = self.agent.ask_question(state_dict)
        # For API, assume all info is in conversation_history; skip Q&A loop
        state_dict["is_complete"] = True
        # Generate document
        state_dict = self.agent.generate_document(state_dict)
        return state_dict.get("final_document", "[No document generated]")

    def refine_document(self, current_draft: str, user_request: str) -> str:
        """
        Use LLM-powered agent to refine a legal document draft.
        """
        import logging
        try:
            return self.agent.refine_document(current_draft, user_request)
        except Exception as e:
            logging.error(f"DraftingService.refine_document error: {e}")
            return f"Error: {e}"

    def extract_details(self, conversation_history: List[Dict[str, str]]) -> dict:
        """
        Use LLM-powered agent to extract structured details from conversation history.
        """
        import logging
        try:
            return self.agent.extract_details(conversation_history)
        except Exception as e:
            logging.error(f"DraftingService.extract_details error: {e}")
            return {"error": str(e)}
