# Legal AI API (FastAPI)

## Overview
This is the FastAPI backend migration of the Legal AI Suite, replacing the previous Streamlit-based implementation. The API contract is strictly based on the previous Django API, with all AI logic ported from the current `drafting`, `clarification`, and `document_qa` modules.

## Structure
- Modular, Django-like FastAPI project
- Endpoints: Auth, Sessions, Messages, AI, Documents
- Pydantic models for request/response validation
- AI services: Only from current codebase (no reuse from old Django backend)

## Setup
```bash
cd legal_ai_api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Migration Notes
- Streamlit and legacy backend code is ignored/excluded
- Endpoints and models match the old API contract
- All AI logic is refactored from the new codebase only
