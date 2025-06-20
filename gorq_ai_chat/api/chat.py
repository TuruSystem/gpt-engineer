from fastapi import APIRouter, Request
from pydantic import BaseModel
from services.model_service import get_model_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    response = get_model_response(req.message)
    return {"response": response}
