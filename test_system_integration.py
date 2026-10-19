"""
VoiceForm AI - Comprehensive End-to-End System Integration Test Suite
Tests backend endpoints, Whisper STT, NLP extraction, Form validation,
Draft & Official PDF generation, and Consented Dataset Management.
"""

import os
import sys
import json
from io import BytesIO

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend to sys.path
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import time
import threading
import requests
import uvicorn
from app.main import app

SERVER_PORT = 8765
BASE_URL = f"http://127.0.0.1:{SERVER_PORT}"

def run_server():
    config = uvicorn.Config(app, host="127.0.0.1", port=SERVER_PORT, log_level="warning")
    server = uvicorn.Server(config)
    server.run()

# Start background server
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Poll until server is ready
for _ in range(20):
    try:
        r = requests.get(f"{BASE_URL}/", timeout=1)
        if r.status_code == 200:
            break
    except Exception:
        time.sleep(0.5)


def run_all_tests():
    print("=" * 80)
    print("        VOICEFORM AI - COMPREHENSIVE SYSTEM INTEGRATION TESTS")
    print("=" * 80)

    tests_run = 0
    tests_passed = 0

    def record_test(name: str, passed: bool, detail: str = ""):
        nonlocal tests_run, tests_passed
        tests_run += 1
        if passed:
            tests_passed += 1
            print(f"  ✅ [PASS] {name} {detail}")
        else:
            print(f"  ❌ [FAIL] {name} - {detail}")

    # 1. Health check GET /
    try:
        r = requests.get(f"{BASE_URL}/")
        ok = r.status_code == 200 and r.json().get("status") == "online"
        record_test("Backend Health Check (GET /)", ok, f"HTTP {r.status_code}")
    except Exception as e:
        record_test("Backend Health Check (GET /)", False, str(e))

    # 2. Sample Audio Endpoint GET /sample-audio
    try:
        r = requests.get(f"{BASE_URL}/sample-audio")
        ok = r.status_code == 200 and len(r.content) > 0
        record_test("Sample Audio Endpoint (GET /sample-audio)", ok, f"Bytes: {len(r.content)}")
    except Exception as e:
        record_test("Sample Audio Endpoint (GET /sample-audio)", False, str(e))

    # 3. Transcribe with empty upload -> Expects 400
    try:
        r = requests.post(f"{BASE_URL}/api/voice/transcribe", files={"file": ("empty.wav", b"", "audio/wav")})
        ok = r.status_code == 400
        record_test("Audio Upload Empty Handling (POST /api/voice/transcribe)", ok, f"HTTP {r.status_code} ({r.json().get('detail')})")
    except Exception as e:
        record_test("Audio Upload Empty Handling", False, str(e))

    # 4. Transcribe with unsupported format -> Expects 400
    try:
        r = requests.post(f"{BASE_URL}/api/voice/transcribe", files={"file": ("bad_file.txt", b"dummy content", "text/plain")})
        ok = r.status_code == 400
        record_test("Audio Upload Unsupported Format Handling", ok, f"HTTP {r.status_code}")
    except Exception as e:
        record_test("Audio Upload Unsupported Format Handling", False, str(e))

    # 5. Transcribe Real Audio Clip (en_1.wav)
    try:
        audio_clip_path = os.path.join(os.path.dirname(__file__), "datasets", "speech", "voiceform_dataset", "audio", "en_1.wav")
        if os.path.exists(audio_clip_path):
            with open(audio_clip_path, "rb") as f:
                r = requests.post(
                    f"{BASE_URL}/api/voice/transcribe",
                    files={"file": ("en_1.wav", f.read(), "audio/wav")},
                    data={"language": "en"}
                )
            data = r.json()
            ok = r.status_code == 200 and "tornado" in data.get("text", "").lower()
            record_test("Whisper Real Audio Transcription (en_1.wav)", ok, f"Recognized: \"{data.get('text')[:45]}...\"")
        else:
            record_test("Whisper Real Audio Transcription (en_1.wav)", False, "File en_1.wav missing on disk")
    except Exception as e:
        record_test("Whisper Real Audio Transcription (en_1.wav)", False, str(e))

    # 6. NLP Entity Extraction (English) with structured_fields
    try:
        sample_text_en = "My name is Rajesh Patil. I am 38 years old. My phone is 9876543210. I am a farmer in Pune Maharashtra. My income is 1.5 lakh."
        r = requests.post(f"{BASE_URL}/api/nlp/extract", json={"text": sample_text_en, "form_id": "pm_kisan"})
        data = r.json()
        struct = data.get("structured_fields", {})
        ok = (
            r.status_code == 200 and
            struct.get("full_name") == "Rajesh Patil" and
            struct.get("age") == 38 and
            struct.get("phone") == "9876543210" and
            struct.get("annual_income") == 150000 and
            struct.get("education") is None  # Verifies null for missing
        )
        record_test("NLP Extraction English & Structured Nulls", ok, f"Name: {struct.get('full_name')}, Age: {struct.get('age')}, Income: {struct.get('annual_income')}")
    except Exception as e:
        record_test("NLP Extraction English & Structured Nulls", False, str(e))

    # 7. NLP Entity Extraction (Hindi)
    try:
        sample_text_hi = "मेरा नाम अमित कुमार है। मेरी उम्र 28 वर्ष है। मैं किसान हूँ और पटना बिहार में रहता हूँ।"
        r = requests.post(f"{BASE_URL}/api/nlp/extract", json={"text": sample_text_hi, "form_id": "income_certificate"})
        data = r.json()
        struct = data.get("structured_fields", {})
        ok = r.status_code == 200 and struct.get("age") == 28 and "Farmer" in str(struct.get("occupation"))
        record_test("NLP Extraction Hindi (उम्र / किसान)", ok, f"Age: {struct.get('age')}, Occ: {struct.get('occupation')}")
    except Exception as e:
        record_test("NLP Extraction Hindi", False, str(e))

    # 8. NLP Entity Extraction (Marathi)
    try:
        sample_text_mr = "माझे नाव सचिन जाधव आहे. माझे वय 42 वर्षे आहे. मी शेतकरी आहे आणि पुणे येथे राहतो."
        r = requests.post(f"{BASE_URL}/api/nlp/extract", json={"text": sample_text_mr, "form_id": "pm_kisan"})
        data = r.json()
        struct = data.get("structured_fields", {})
        ok = r.status_code == 200 and struct.get("age") == 42 and "Farmer" in str(struct.get("occupation"))
        record_test("NLP Extraction Marathi (वय / शेतकरी)", ok, f"Age: {struct.get('age')}, Occ: {struct.get('occupation')}")
    except Exception as e:
        record_test("NLP Extraction Marathi", False, str(e))

    # 9. Government Forms Listing & Retrieval GET /api/forms
    try:
        r = requests.get(f"{BASE_URL}/api/forms")
        forms = r.json().get("forms", [])
        ok = r.status_code == 200 and len(forms) >= 3
        record_test("Government Forms Catalog (GET /api/forms)", ok, f"Found {len(forms)} configured forms")
    except Exception as e:
        record_test("Government Forms Catalog", False, str(e))

    # 10. Form Validation - Missing Required Fields Check
    try:
        incomplete_data = {
            "applicant_name": "Ramesh Patil"
            # Missing mobile, aadhaar, annual income, etc.
        }
        r = requests.post(f"{BASE_URL}/api/forms/validate", json={"form_id": "income_certificate", "form_data": incomplete_data})
        data = r.json()
        missing = data.get("missing_fields", [])
        ok = r.status_code == 200 and data.get("is_valid") is False and len(missing) > 0
        record_test("Form Validation Missing Fields Flagging", ok, f"Flagged {len(missing)} missing mandatory fields")
    except Exception as e:
        record_test("Form Validation Missing Fields Flagging", False, str(e))

    # 11. Download Draft PDF (POST /api/forms/draft-pdf)
    try:
        r = requests.post(
            f"{BASE_URL}/api/forms/draft-pdf",
            json={
                "form_id": "income_certificate",
                "form_data": {"applicant_name": "Ramesh Patil", "state": "Maharashtra"}
            }
        )
        ok = r.status_code == 200 and r.headers.get("content-type") == "application/pdf" and len(r.content) > 1000
        record_test("Draft PDF Preview Generation (POST /api/forms/draft-pdf)", ok, f"PDF Size: {len(r.content)} bytes")
    except Exception as e:
        record_test("Draft PDF Preview Generation", False, str(e))

    # 12. Submit Form (POST /api/forms/submit)
    created_app_id = None
    try:
        submission_payload = {
            "form_id": "income_certificate",
            "form_data": {
                "applicant_name": "Ramesh Shankar Patil",
                "applicant_age": 42,
                "applicant_gender": "Male",
                "aadhaar_number": "5432 8765 1290",
                "mobile_number": "9876543210",
                "residential_address": "Shivaji Nagar, Pune",
                "district": "Pune",
                "state": "Maharashtra",
                "pincode": "411005",
                "applicant_occupation": "Farmer / Shetkari / Kisan",
                "annual_income": 120000,
                "social_category": "OBC (Other Backward Class)"
            },
            "raw_transcript": "My name is Ramesh Shankar Patil...",
            "language": "en"
        }
        r = requests.post(f"{BASE_URL}/api/forms/submit", json=submission_payload)
        data = r.json()
        created_app_id = data.get("application_id")
        ok = r.status_code == 200 and created_app_id is not None and "VF-" in created_app_id
        record_test("Application Form Submission & Reference Generation", ok, f"Ref ID: {created_app_id}")
    except Exception as e:
        record_test("Application Form Submission", False, str(e))

    # 13. Official Submitted PDF Receipt (GET /api/forms/submissions/{id}/pdf)
    if created_app_id:
        try:
            r = requests.get(f"{BASE_URL}/api/forms/submissions/{created_app_id}/pdf")
            ok = r.status_code == 200 and r.headers.get("content-type") == "application/pdf" and len(r.content) > 1000
            record_test("Official Submitted Receipt PDF (GET .../pdf)", ok, f"PDF Size: {len(r.content)} bytes")
        except Exception as e:
            record_test("Official Submitted Receipt PDF", False, str(e))

    # 14. Dataset Status Overview (GET /api/dataset/status)
    try:
        r = requests.get(f"{BASE_URL}/api/dataset/status")
        data = r.json()
        ok = r.status_code == 200 and data.get("success") is True and "speech_dataset" in data
        record_test("Dataset Status Overview (GET /api/dataset/status)", ok, f"FLEURS: {data['speech_dataset']['total_fleurs_clips']} clips")
    except Exception as e:
        record_test("Dataset Status Overview", False, str(e))

    # 15. Dataset Integrity Validation Endpoint (GET /api/dataset/validate)
    try:
        r = requests.get(f"{BASE_URL}/api/dataset/validate?limit=3")
        data = r.json()
        report = data.get("report", {})
        ok = r.status_code == 200 and report.get("status") in ["PASSED", "PASSED_WITH_WARNINGS"]
        record_test("Dataset Validation API (GET /api/dataset/validate)", ok, f"Status: {report.get('status')}")
    except Exception as e:
        record_test("Dataset Validation API", False, str(e))

    # 16. Consented Audio Contribution Without Consent -> Expects 400
    try:
        dummy_wav = b"RIFF....WAVEfmt ...."
        r = requests.post(
            f"{BASE_URL}/api/dataset/samples",
            files={"file": ("sample.wav", dummy_wav, "audio/wav")},
            data={"language": "en", "transcript": "Testing sample", "consent_given": "false"}
        )
        ok = r.status_code == 400
        record_test("Consent Enforcement (No Consent Rejected)", ok, f"HTTP {r.status_code}")
    except Exception as e:
        record_test("Consent Enforcement", False, str(e))

    # 17. Consented Audio Contribution With Consent -> Expects 200
    created_sample_id = None
    try:
        real_wav_path = os.path.join(os.path.dirname(__file__), "datasets", "speech", "voiceform_dataset", "audio", "en_1.wav")
        with open(real_wav_path, "rb") as f:
            wav_bytes = f.read()

        r = requests.post(
            f"{BASE_URL}/api/dataset/samples",
            files={"file": ("consented_test.wav", wav_bytes, "audio/wav")},
            data={"language": "en", "transcript": "Consented demonstration sample", "consent_given": "true"}
        )
        data = r.json()
        created_sample_id = data.get("sample", {}).get("id")
        ok = r.status_code == 200 and created_sample_id is not None
        record_test("Consented Sample Recording (POST /api/dataset/samples)", ok, f"Sample ID: {created_sample_id}")
    except Exception as e:
        record_test("Consented Sample Recording", False, str(e))

    # 18. Sample Review & Approval (POST /api/dataset/samples/{id}/review)
    if created_sample_id:
        try:
            r = requests.post(
                f"{BASE_URL}/api/dataset/samples/{created_sample_id}/review",
                json={"review_status": "APPROVED", "notes": "Verified demonstration clip"}
            )
            ok = r.status_code == 200 and r.json().get("status") == "APPROVED"
            record_test("Sample Human Review & Approval (POST .../review)", ok, f"Status: APPROVED")
        except Exception as e:
            record_test("Sample Human Review & Approval", False, str(e))

    # 19. Export Approved Samples to CSV (GET /api/dataset/export)
    try:
        r = requests.get(f"{BASE_URL}/api/dataset/export")
        ok = r.status_code == 200 and "sample_id,audio_filename" in r.text
        record_test("Approved Dataset CSV Export (GET /api/dataset/export)", ok, f"CSV Rows: {len(r.text.splitlines())}")
    except Exception as e:
        record_test("Approved Dataset CSV Export", False, str(e))

    # 20. Sample Deletion (DELETE /api/dataset/samples/{id})
    if created_sample_id:
        try:
            r = requests.delete(f"{BASE_URL}/api/dataset/samples/{created_sample_id}")
            ok = r.status_code == 200 and r.json().get("success") is True
            record_test("Sample Deletion for Privacy (DELETE .../samples)", ok, "Cleaned metadata and audio file")
        except Exception as e:
            record_test("Sample Deletion for Privacy", False, str(e))

    # 21. Form Extraction Held-Out Test Evaluation API
    try:
        r = requests.get(f"{BASE_URL}/api/dataset/form-extraction/evaluate?split=test")
        data = r.json()
        results = data.get("results", {})
        f1 = results.get("overall_micro_metrics", {}).get("f1", 0)
        ok = r.status_code == 200 and f1 > 0.8
        record_test("Form Extraction Test Evaluation API (GET .../evaluate)", ok, f"Held-out F1: {f1 * 100:.1f}%")
    except Exception as e:
        record_test("Form Extraction Test Evaluation API", False, str(e))

    print("-" * 80)
    print(f"Test Suite Summary: {tests_passed} / {tests_run} Passed ({(tests_passed/tests_run)*100:.1f}%)")
    print("=" * 80)
    return tests_passed == tests_run

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
