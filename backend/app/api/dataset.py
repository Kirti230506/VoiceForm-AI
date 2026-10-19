"""
VoiceForm AI - Dataset Management API
Endpoints for speech dataset status, validation, consented sample collection,
human review, approval, CSV export, sample deletion, and form extraction dataset access.
"""

import os
import io
import csv
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ConsentedAudioSample
from app.services.speech_service import ALLOWED_AUDIO_EXTENSIONS, MAX_AUDIO_SIZE_BYTES

# Import validator logic
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from validate_dataset import validate_dataset
from evaluate_form_extraction import evaluate_form_extraction

router = APIRouter()

COLLECTED_DIR = os.path.join(ROOT_DIR, "datasets", "speech", "collected")
COLLECTED_AUDIO_DIR = os.path.join(COLLECTED_DIR, "audio")
FORM_EXTRACTION_FILE = os.path.join(ROOT_DIR, "datasets", "form_extraction", "form_extraction_dataset.json")

def ensure_collected_dirs():
    os.makedirs(COLLECTED_AUDIO_DIR, exist_ok=True)

class ReviewSampleRequest(BaseModel):
    review_status: str  # APPROVED, REJECTED, PENDING
    transcript: Optional[str] = None
    notes: Optional[str] = None

@router.get("/status")
def get_dataset_overview(db: Session = Depends(get_db)):
    """Returns real-time status of speech datasets and form extraction datasets."""
    speech_validation = validate_dataset(max_audio_checks=1)

    collected_total = db.query(ConsentedAudioSample).count()
    collected_approved = db.query(ConsentedAudioSample).filter(ConsentedAudioSample.review_status == "APPROVED").count()
    collected_pending = db.query(ConsentedAudioSample).filter(ConsentedAudioSample.review_status == "PENDING").count()

    form_extraction_count = 0
    if os.path.exists(FORM_EXTRACTION_FILE):
        import json
        with open(FORM_EXTRACTION_FILE, "r", encoding="utf-8") as f:
            form_extraction_count = len(json.load(f))

    return {
        "success": True,
        "speech_dataset": {
            "status": speech_validation.get("status"),
            "location": speech_validation.get("dataset_path"),
            "total_fleurs_clips": speech_validation.get("total_rows", 0),
            "languages": speech_validation.get("languages_count", {}),
            "audio_files_disk": speech_validation.get("audio_files_found_on_disk", 0)
        },
        "consented_collection": {
            "total_collected": collected_total,
            "approved": collected_approved,
            "pending_review": collected_pending,
            "storage_folder": COLLECTED_DIR
        },
        "form_extraction_dataset": {
            "total_labeled_samples": form_extraction_count,
            "file": FORM_EXTRACTION_FILE
        }
    }

@router.get("/validate")
def run_dataset_validation(limit: int = 5):
    """Executes dataset integrity validation on speech clips."""
    res = validate_dataset(max_audio_checks=limit)
    return {
        "success": True,
        "report": res
    }

@router.post("/samples")
async def collect_sample(
    file: UploadFile = File(...),
    language: str = Form("en"),
    transcript: str = Form(""),
    consent_given: bool = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Submits a consented, user-reviewed voice recording into the development dataset.
    Requires explicit informed consent.
    """
    if not consent_given:
        raise HTTPException(
            status_code=400,
            detail="Explicit informed consent is required to save audio samples for model improvement."
        )

    if not file.filename:
        raise HTTPException(status_code=400, detail="Audio file is required.")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext and ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format '{ext}'.")

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded audio is empty.")
    if len(contents) > MAX_AUDIO_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="Audio exceeds 25 MB limit.")

    ensure_collected_dirs()
    year = datetime.now().year
    sample_id = f"SMP-{year}-{uuid.uuid4().hex[:8].upper()}"
    saved_filename = f"{sample_id}_{language}{ext or '.wav'}"
    target_path = os.path.join(COLLECTED_AUDIO_DIR, saved_filename)

    with open(target_path, "wb") as f:
        f.write(contents)

    rel_path = os.path.relpath(target_path, ROOT_DIR)

    sample = ConsentedAudioSample(
        id=sample_id,
        audio_filename=saved_filename,
        audio_relpath=rel_path,
        language=language,
        transcript=transcript.strip(),
        review_status="PENDING",
        consent_given=True,
        notes=notes,
        created_at=datetime.utcnow()
    )

    db.add(sample)
    db.commit()
    db.refresh(sample)

    return {
        "success": True,
        "message": "Sample successfully recorded with informed consent and queued for review.",
        "sample": {
            "id": sample.id,
            "filename": sample.audio_filename,
            "language": sample.language,
            "transcript": sample.transcript,
            "status": sample.review_status,
            "created_at": sample.created_at.isoformat()
        }
    }

@router.get("/samples")
def list_collected_samples(
    status: Optional[str] = None,
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lists consented audio samples for review and administrative inspection."""
    query = db.query(ConsentedAudioSample)
    if status:
        query = query.filter(ConsentedAudioSample.review_status == status.upper())
    if language:
        query = query.filter(ConsentedAudioSample.language == language.lower())

    samples = query.order_by(ConsentedAudioSample.created_at.desc()).all()
    return {
        "success": True,
        "total": len(samples),
        "samples": [
            {
                "id": s.id,
                "filename": s.audio_filename,
                "language": s.language,
                "transcript": s.transcript,
                "review_status": s.review_status,
                "consent_given": s.consent_given,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "reviewed_at": s.reviewed_at.isoformat() if s.reviewed_at else None,
                "notes": s.notes
            }
            for s in samples
        ]
    }

@router.post("/samples/{sample_id}/review")
def review_sample(
    sample_id: str,
    payload: ReviewSampleRequest,
    db: Session = Depends(get_db)
):
    """Allows authorized review (Approve / Reject) and transcript correction."""
    sample = db.query(ConsentedAudioSample).filter(ConsentedAudioSample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found.")

    valid_statuses = {"APPROVED", "REJECTED", "PENDING"}
    new_status = payload.review_status.upper()
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {valid_statuses}")

    sample.review_status = new_status
    if payload.transcript is not None:
        sample.transcript = payload.transcript.strip()
    if payload.notes is not None:
        sample.notes = payload.notes.strip()
    sample.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(sample)

    return {
        "success": True,
        "message": f"Sample {sample_id} status updated to {new_status}.",
        "sample_id": sample.id,
        "status": sample.review_status
    }

@router.delete("/samples/{sample_id}")
def delete_sample(sample_id: str, db: Session = Depends(get_db)):
    """Permanently deletes a retained audio recording and metadata upon user request."""
    sample = db.query(ConsentedAudioSample).filter(ConsentedAudioSample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found.")

    # Remove audio file from disk if present
    abs_audio = os.path.join(ROOT_DIR, sample.audio_relpath)
    if os.path.exists(abs_audio):
        try:
            os.remove(abs_audio)
        except Exception as e:
            pass

    db.delete(sample)
    db.commit()

    return {
        "success": True,
        "message": f"Sample {sample_id} and associated audio file were permanently deleted."
    }

@router.get("/export")
def export_approved_dataset_csv(db: Session = Depends(get_db)):
    """Exports approved consented samples to CSV format."""
    approved_samples = db.query(ConsentedAudioSample).filter(
        ConsentedAudioSample.review_status == "APPROVED"
    ).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["sample_id", "audio_filename", "language", "transcript", "created_at", "consent_status"])

    for s in approved_samples:
        writer.writerow([
            s.id,
            s.audio_filename,
            s.language,
            s.transcript,
            s.created_at.isoformat() if s.created_at else "",
            "CONSENTED"
        ])

    csv_data = output.getvalue()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=approved_voiceform_samples.csv"
        }
    )

@router.get("/form-extraction")
def get_form_extraction_samples():
    """Returns the synthetic labeled form-extraction dataset."""
    if not os.path.exists(FORM_EXTRACTION_FILE):
        return {"success": True, "samples": []}
    import json
    with open(FORM_EXTRACTION_FILE, "r", encoding="utf-8") as f:
        samples = json.load(f)
    return {
        "success": True,
        "total": len(samples),
        "samples": samples
    }

@router.get("/form-extraction/evaluate")
def run_form_extraction_eval(split: str = "test"):
    """Runs field-level evaluation on held-out form-extraction test split."""
    results = evaluate_form_extraction(split=split)
    return {
        "success": True,
        "results": results
    }
