import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ApplicationSubmission
from app.services.form_service import get_all_forms, get_form_by_id, auto_fill_form
from app.services.assistant_service import validate_form_data
from app.services.pdf_generator import generate_application_pdf, generate_draft_pdf


router = APIRouter()

class FormSubmissionRequest(BaseModel):
    form_id: str
    form_data: Dict[str, Any]
    extracted_entities: Optional[Dict[str, Any]] = None
    raw_transcript: Optional[str] = None
    language: Optional[str] = "en"

class ValidateFormRequest(BaseModel):
    form_id: str
    form_data: Dict[str, Any]

@router.get("")
def list_forms():
    return {
        "success": True,
        "forms": get_all_forms()
    }

@router.get("/{form_id}")
def get_form(form_id: str):
    form = get_form_by_id(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return {
        "success": True,
        "form": form
    }

@router.post("/validate")
def validate_form(payload: ValidateFormRequest):
    form_def = get_form_by_id(payload.form_id)
    if not form_def:
        raise HTTPException(status_code=404, detail="Form not found")

    res = validate_form_data(payload.form_id, payload.form_data, form_def)
    return {
        "success": True,
        **res
    }

@router.post("/draft-pdf")
def download_draft_pdf(payload: ValidateFormRequest):
    form_def = get_form_by_id(payload.form_id)
    if not form_def:
        raise HTTPException(status_code=404, detail="Form not found")

    val_res = validate_form_data(payload.form_id, payload.form_data, form_def)
    pdf_buffer = generate_draft_pdf(form_def, payload.form_data, val_res)

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=Draft_{payload.form_id}.pdf"
        }
    )


@router.post("/submit")
def submit_form(payload: FormSubmissionRequest, db: Session = Depends(get_db)):
    form_def = get_form_by_id(payload.form_id)
    if not form_def:
        raise HTTPException(status_code=404, detail="Form not found")

    # Generate unique reference ID
    year = datetime.now().year
    app_id = f"VF-{year}-{uuid.uuid4().hex[:8].upper()}"

    applicant_name = (
        payload.form_data.get("applicant_name") or
        (payload.extracted_entities.get("fullName", {}).get("value") if payload.extracted_entities else None)
    )
    applicant_phone = (
        payload.form_data.get("mobile_number") or
        (payload.extracted_entities.get("phone", {}).get("value") if payload.extracted_entities else None)
    )
    applicant_aadhaar = (
        payload.form_data.get("aadhaar_number") or
        (payload.extracted_entities.get("aadhaar", {}).get("value") if payload.extracted_entities else None)
    )

    submission = ApplicationSubmission(
        id=app_id,
        form_id=payload.form_id,
        form_name=form_def["title"],
        applicant_name=applicant_name,
        applicant_phone=applicant_phone,
        applicant_aadhaar=applicant_aadhaar,
        status="SUBMITTED",
        form_data=payload.form_data,
        extracted_entities=payload.extracted_entities,
        raw_transcript=payload.raw_transcript,
        language=payload.language,
        submitted_at=datetime.utcnow(),
        verification_hash=uuid.uuid4().hex
    )

    try:
        db.add(submission)
        db.commit()
        db.refresh(submission)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error during submission: {str(e)}")

    return {
        "success": True,
        "message": "Application submitted successfully",
        "application_id": app_id,
        "form_id": payload.form_id,
        "form_name": form_def["title"],
        "applicant_name": applicant_name,
        "submitted_at": submission.submitted_at.isoformat(),
        "status": submission.status,
        "next_steps": [
            "Your application has been registered with the Central Citizen Service Gateway.",
            "SMS notification has been triggered with tracking number.",
            "Document scrutiny will be performed by the designated Tehsildar / Nodal Officer.",
            "Download your official PDF acknowledgment receipt below."
        ]
    }

@router.get("/submissions/{submission_id}")
def get_submission(submission_id: str, db: Session = Depends(get_db)):
    sub = db.query(ApplicationSubmission).filter(ApplicationSubmission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission record not found")

    return {
        "success": True,
        "submission": {
            "id": sub.id,
            "form_id": sub.form_id,
            "form_name": sub.form_name,
            "applicant_name": sub.applicant_name,
            "applicant_phone": sub.applicant_phone,
            "status": sub.status,
            "form_data": sub.form_data,
            "submitted_at": sub.submitted_at.isoformat() if sub.submitted_at else None,
            "verification_hash": sub.verification_hash
        }
    }

@router.get("/submissions/{submission_id}/pdf")
def download_submission_pdf(submission_id: str, db: Session = Depends(get_db)):
    sub = db.query(ApplicationSubmission).filter(ApplicationSubmission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission record not found")

    sub_dict = {
        "id": sub.id,
        "form_name": sub.form_name,
        "applicant_name": sub.applicant_name,
        "status": sub.status,
        "submitted_at": sub.submitted_at.isoformat() if sub.submitted_at else None,
        "form_data": sub.form_data or {}
    }

    pdf_buffer = generate_application_pdf(sub_dict)

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=VoiceForm_Receipt_{sub.id}.pdf"
        }
    )
