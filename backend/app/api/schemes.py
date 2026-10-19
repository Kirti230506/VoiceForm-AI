from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.services.scheme_engine import SCHEMES_CATALOG, evaluate_scheme_eligibility, DISCLAIMER_TEXT
from app.services.nlp_engine import extract_all_entities

router = APIRouter()

class ProfileCheckRequest(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    annualIncome: Optional[int] = None
    occupation: Optional[str] = None
    socialCategory: Optional[str] = None
    state: Optional[str] = None
    landHolding: Optional[str] = None
    raw_speech_text: Optional[str] = None

@router.get("")
def list_schemes(category: Optional[str] = None):
    schemes = SCHEMES_CATALOG
    if category and category.lower() != "all":
        schemes = [s for s in schemes if s["category"].lower() == category.lower()]

    return {
        "success": True,
        "count": len(schemes),
        "schemes": schemes,
        "disclaimer": DISCLAIMER_TEXT
    }

@router.get("/{scheme_id}")
def get_scheme(scheme_id: str):
    for s in SCHEMES_CATALOG:
        if s["id"] == scheme_id:
            return {"success": True, "scheme": s, "disclaimer": DISCLAIMER_TEXT}
    raise HTTPException(status_code=404, detail="Scheme not found")

@router.post("/check-eligibility")
def check_eligibility(payload: ProfileCheckRequest):
    # If raw speech text is provided, extract profile values using NLP
    user_profile = {
        "age": payload.age,
        "gender": payload.gender,
        "annualIncome": payload.annualIncome,
        "occupation": payload.occupation,
        "socialCategory": payload.socialCategory,
        "state": payload.state,
        "landHolding": payload.landHolding
    }

    extracted_from_speech = {}
    if payload.raw_speech_text:
        speech_extraction = extract_all_entities(payload.raw_speech_text)
        entities = speech_extraction.get("entities", {})
        extracted_from_speech = entities

        # Populate missing values from speech
        if user_profile["age"] is None and "age" in entities:
            user_profile["age"] = entities["age"]["value"]
        if not user_profile["gender"] and "gender" in entities:
            user_profile["gender"] = entities["gender"]["value"]
        if user_profile["annualIncome"] is None and "annualIncome" in entities:
            user_profile["annualIncome"] = entities["annualIncome"]["value"]
        if not user_profile["occupation"] and "occupation" in entities:
            user_profile["occupation"] = entities["occupation"]["value"]
        if not user_profile["socialCategory"] and "socialCategory" in entities:
            user_profile["socialCategory"] = entities["socialCategory"]["value"]
        if not user_profile["state"] and "state" in entities:
            user_profile["state"] = entities["state"]["value"]
        if not user_profile["landHolding"] and "landHolding" in entities:
            user_profile["landHolding"] = entities["landHolding"]["value"]

    result = evaluate_scheme_eligibility(user_profile)

    return {
        "success": True,
        "extracted_from_speech": extracted_from_speech,
        **result
    }
