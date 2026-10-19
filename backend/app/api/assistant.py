from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.assistant_service import explain_field, answer_query

router = APIRouter()

class ChatQueryRequest(BaseModel):
    query: str
    language: Optional[str] = "en"

@router.get("/explain")
def get_field_explanation(field_id: str, lang: Optional[str] = "en"):
    res = explain_field(field_id, lang)
    return {
        "success": True,
        **res
    }

@router.post("/chat")
def ask_assistant(payload: ChatQueryRequest):
    res = answer_query(payload.query, payload.language or "en")
    return {
        "success": True,
        **res
    }
