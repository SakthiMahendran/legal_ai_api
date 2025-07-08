from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# --- Auth ---

class RefreshResponse(BaseModel):
    access_token: str

class LogoutRequest(BaseModel):
    pass

class LogoutResponse(BaseModel):
    success: bool
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class RegisterResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access: str
    refresh: str

class RefreshRequest(BaseModel):
    refresh: str

# --- Session ---
class SessionModel(BaseModel):
    id: str
    title: str
    status: str
    created_at: datetime
    updated_at: datetime

class CreateSessionRequest(BaseModel):
    title: str
    status: str

# --- Message ---
class MessageModel(BaseModel):
    id: str
    session: str
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

class CreateMessageRequest(BaseModel):
    session: str
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

# --- AI ---
class GenerateRequest(BaseModel):
    prompt: str
    conversation_history: List[Dict[str, str]]

class GenerateResponse(BaseModel):
    result: str

class RefineRequest(BaseModel):
    current_draft: str
    user_request: str

class ExtractDetailsRequest(BaseModel):
    conversation_history: List[Dict[str, str]]

class ExtractDetailsResponse(BaseModel):
    details: Dict[str, Any]

class AIHealthResponse(BaseModel):
    status: str
    ai_configured: bool
    modules_loaded: bool
    debug_mode: bool

# --- Document ---
class DocumentModel(BaseModel):
    id: str
    session: str
    document_type: str
    content: str
    formatted_content: Optional[str]
    created_at: datetime
    updated_at: datetime

class CreateDocumentRequest(BaseModel):
    session: str
    document_type: str
    content: str
    formatted_content: Optional[str] = None

class GenerateFormattedDocumentResponse(BaseModel):
    message: str
    formatted_content: str

class DocumentDetailsRequest(BaseModel):
    document: str
    details: Dict[str, Any]
    verified: bool

# --- Error ---
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
