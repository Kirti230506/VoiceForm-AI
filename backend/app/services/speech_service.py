"""
VoiceForm AI - Speech Recognition Service
Encapsulates Whisper model loading, audio validation, transcription,
language parameter handling, and safe error reporting.
"""

import os
import re
import asyncio
import logging
import tempfile
from typing import Dict, Any, Optional
import whisper

logger = logging.getLogger("voiceform.speech")

MAX_AUDIO_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB
ALLOWED_AUDIO_EXTENSIONS = {".wav", ".webm", ".mp3", ".m4a", ".ogg", ".flac", ".aac"}
LANGUAGE_CODE_MAP = {
    "en": "en",
    "english": "en",
    "hi": "hi",
    "hindi": "hi",
    "mr": "mr",
    "marathi": "mr"
}

LANGUAGE_PROMPTS = {
    "en": "Indian citizen government application form details: full name, age, mobile number, 12-digit Aadhaar, occupation, farmer, shetkari, kisan, annual income in lakh, district, state, Pune, Maharashtra, Bihar, Uttar Pradesh.",
    "hi": "भारतीय सरकारी फॉर्म आवेदन: मेरा नाम, उम्र, वर्ष, मोबाइल नंबर, आधार कार्ड, किसान, मजदूर, वार्षिक आय, लाख, हजार, जिला, राज्य, जाति, पता।",
    "mr": "शासकीय अर्ज माहिती: माझे नाव, वय, वर्षे, मोबाईल क्रमांक, आधार कार्ड, शेतकरी, वार्षिक उत्पन्न, लाख, हजार, जिल्हा, राज्य, जात, शिक्षण, पत्ता।"
}

# Lazy or module-level Whisper model singleton
_whisper_model = None

def get_whisper_model(model_name: str = "base"):
    global _whisper_model
    if _whisper_model is None:
        logger.info(f"[SpeechService] Loading Whisper '{model_name}' model...")
        _whisper_model = whisper.load_model(model_name)
        logger.info("[SpeechService] Whisper model loaded successfully.")
    return _whisper_model

def sanitize_repetition(text: str) -> str:
    """Detects and cleans pathological repeating token hallucinations."""
    if not text:
        return ""
    words = text.split()
    if len(words) > 8:
        # Check if 70%+ of words are the same token
        most_common = max(set(words), key=words.count)
        if words.count(most_common) / len(words) > 0.65:
            return ""
    return text.strip()

def transcribe_audio_file_sync(
    file_bytes: bytes,
    filename: Optional[str] = None,
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Synchronous audio transcription logic for threadpool execution.
    Performs format checks, size checks, and safe tempfile cleanup.
    """
    if not file_bytes or len(file_bytes) == 0:
        raise ValueError("Audio recording is empty. Please speak into the microphone or upload a valid audio file.")

    if len(file_bytes) > MAX_AUDIO_SIZE_BYTES:
        raise ValueError("Audio file size exceeds the 25 MB limit.")

    suffix = ".wav"
    if filename:
        ext = os.path.splitext(filename)[1].lower()
        if ext in ALLOWED_AUDIO_EXTENSIONS:
            suffix = ext
        elif ext:
            raise ValueError(f"Unsupported audio format '{ext}'. Supported formats: WAV, WebM, MP3, M4A, OGG, FLAC.")

    # Determine language parameter
    whisper_lang = None
    if language:
        lang_key = language.strip().lower()
        whisper_lang = LANGUAGE_CODE_MAP.get(lang_key)

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(file_bytes)
            temp_path = temp.name

        model = get_whisper_model()
        options = {
            "fp16": False,
            "condition_on_previous_text": False,
            "compression_ratio_threshold": 2.4,
            "no_speech_threshold": 0.6,
        }
        if whisper_lang:
            options["language"] = whisper_lang
            if whisper_lang in LANGUAGE_PROMPTS:
                options["initial_prompt"] = LANGUAGE_PROMPTS[whisper_lang]
        else:
            options["initial_prompt"] = LANGUAGE_PROMPTS["en"]

        result = model.transcribe(temp_path, **options)
        raw_text = result.get("text", "").strip()
        cleaned_text = sanitize_repetition(raw_text)
        detected_lang = result.get("language", whisper_lang or "en")

        return {
            "success": True,
            "text": cleaned_text,
            "raw_text": raw_text,
            "detected_language": detected_lang,
            "is_empty": len(cleaned_text) == 0,
            "message": "Transcription completed successfully." if cleaned_text else "No clear speech detected. Please speak closer to the microphone and try again."
        }
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Whisper transcription failed: {e}")
        # Sanitize internal filesystem paths out of user error message
        err_msg = str(e)
        if "temp" in err_msg.lower() or "file" in err_msg.lower() or "\\" in err_msg or "/" in err_msg:
            err_msg = "Audio processing or decoding error. Ensure audio is recorded properly."
        raise RuntimeError(f"Speech recognition error: {err_msg}")
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.warning(f"Failed to remove temp file: {e}")

async def transcribe_audio_async(
    file_bytes: bytes,
    filename: Optional[str] = None,
    language: Optional[str] = None
) -> Dict[str, Any]:
    """Asynchronous wrapper running transcription on a worker thread to prevent event loop blocking."""
    return await asyncio.to_thread(transcribe_audio_file_sync, file_bytes, filename, language)
