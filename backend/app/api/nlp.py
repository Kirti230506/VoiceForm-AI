from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.nlp_engine import extract_all_entities
from app.services.form_service import auto_fill_form

router = APIRouter()

class ExtractRequest(BaseModel):
    text: str
    form_id: Optional[str] = "income_certificate"
    existing_data: Optional[Dict[str, Any]] = None

@router.post("/extract")
def extract_from_text(payload: ExtractRequest):
    extraction = extract_all_entities(payload.text)
    
    target_form = payload.form_id or extraction.get("detected_intent") or "income_certificate"
    fill_result = auto_fill_form(target_form, extraction["entities"], payload.existing_data)

    return {
        "success": True,
        "raw_text": extraction["raw_text"],
        "extracted_entities": extraction["entities"],
        "entities_count": extraction["entities_count"],
        "structured_fields": extraction.get("structured_fields", {}),
        "needs_confirmation": extraction.get("needs_confirmation", False),
        "detected_intent": extraction.get("detected_intent"),
        "target_form_id": target_form,
        "mapped_form_data": fill_result.get("form_data", {}),
        "mapped_fields": fill_result.get("mapped_fields", {})
    }
