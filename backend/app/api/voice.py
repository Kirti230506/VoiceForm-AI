import os
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from app.services.speech_service import transcribe_audio_async, ALLOWED_AUDIO_EXTENSIONS, MAX_AUDIO_SIZE_BYTES
from app.services.nlp_engine import extract_all_entities
from app.services.form_service import auto_fill_form

logger = logging.getLogger("voice")
router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None)
):
    """
    Transcribes uploaded audio (WAV, WebM, MP3, etc.) using OpenAI Whisper.
    Validates file format, size limits, and prevents event-loop blocking.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No audio file provided.")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext and ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{ext}'. Supported formats: {', '.join(sorted(ALLOWED_AUDIO_EXTENSIONS))}."
        )

    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Uploaded audio file is empty.")
        if len(contents) > MAX_AUDIO_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="Audio file exceeds 25 MB limit.")

        result = await transcribe_audio_async(contents, filename=file.filename, language=language)
        return {
            "success": True,
            "filename": file.filename,
            "text": result["text"],
            "raw_text": result.get("raw_text", ""),
            "detected_language": result["detected_language"],
            "is_empty": result.get("is_empty", False),
            "message": result.get("message", "")
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=f"Audio transcription error: {str(e)}")

@router.post("/extract-and-fill")
async def extract_and_fill(
    file: UploadFile = File(...),
    form_id: Optional[str] = Form("income_certificate"),
    language: Optional[str] = Form(None)
):
    """
    Transcribes audio with Whisper, extracts structured entities with NLP/NER,
    and returns mapped form data ready for auto-filling.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No audio file provided.")

    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Uploaded audio file is empty.")
        if len(contents) > MAX_AUDIO_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="Audio file exceeds 25 MB limit.")

        trans_result = await transcribe_audio_async(contents, filename=file.filename, language=language)
        transcribed_text = trans_result["text"]

        # Run NLP/NER Information Extraction on the recognized text
        extraction_result = extract_all_entities(transcribed_text)

        # Map to active form
        target_form = form_id or extraction_result.get("detected_intent") or "income_certificate"
        fill_result = auto_fill_form(target_form, extraction_result["entities"])

        return {
            "success": True,
            "transcribed_text": transcribed_text,
            "detected_language": trans_result["detected_language"],
            "extracted_entities": extraction_result["entities"],
            "entities_count": extraction_result["entities_count"],
            "detected_intent": extraction_result.get("detected_intent"),
            "target_form_id": target_form,
            "mapped_form_data": fill_result.get("form_data", {}),
            "mapped_fields": fill_result.get("mapped_fields", {})
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Extract and fill error: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")