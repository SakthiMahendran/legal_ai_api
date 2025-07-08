from fastapi import APIRouter, status
from legal_ai_api.app.models.pydantic_schemas import GenerateRequest, GenerateResponse, RefineRequest, ExtractDetailsRequest, ExtractDetailsResponse, AIHealthResponse
from fastapi.responses import JSONResponse

router = APIRouter()

from legal_ai_api.app.services.drafting_service import DraftingService

drafting_service = DraftingService()

@router.post('/generate/', response_model=GenerateResponse)
def generate_document(request: GenerateRequest):
    """
    Generate a legal document using the DraftingService (LLM agent).
    """
    result = drafting_service.generate_document(
        prompt=request.prompt,
        conversation_history=request.conversation_history
    )
    return GenerateResponse(result=result)

@router.post('/refine/', response_model=GenerateResponse)
def refine_document(request: RefineRequest):
    """
    Refine a legal document draft using the DraftingService (LLM agent).
    """
    result = drafting_service.refine_document(
        current_draft=request.current_draft,
        user_request=request.user_request
    )
    return GenerateResponse(result=result)

@router.post('/extract-details/', response_model=ExtractDetailsResponse)
def extract_details(request: ExtractDetailsRequest):
    """
    Extract structured details from conversation history using the DraftingService.
    """
    details = drafting_service.extract_details(request.conversation_history)
    return ExtractDetailsResponse(**details)

@router.get('/health/', response_model=AIHealthResponse)
def ai_health():
    # TODO: Implement AI health check
    return JSONResponse(content={"detail": "Not implemented"}, status_code=501)

