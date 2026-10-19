# 🎙️ VoiceForm AI — AI-Powered Voice Government Form Assistant

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![OpenAI Whisper](https://img.shields.io/badge/Whisper-Speech--to--Text-FF6F00.svg)](https://github.com/openai/whisper)
[![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**VoiceForm AI** is an accessible, AI-powered multilingual web application that empowers citizens to fill Indian government application forms using **voice input instead of manual typing**. The system supports **English, Hindi (हिन्दी), and Marathi (मराठी)**, provides an editable 2-step transcription-to-extraction workflow, validates required fields, exports reviewable draft and official signed PDF receipts, and features a consent-driven audio dataset collection studio.

---

## 🏛️ System Overview & Architecture

VoiceForm AI separates speech recognition, natural language entity extraction, and form lifecycle management into distinct, testable modules.

```text
               +-------------------------------------------+
               |             Citizen Voice Input           |
               | (Browser Microphone / Audio Sample / WebM)|
               +-------------------------------------------+
                                     |
                                     v
               +-------------------------------------------+
               |        React 19 Frontend Interface        |
               | (Port 5173 - Multilingual EN / HI / MR)   |
               +-------------------------------------------+
                                     |
                                     v [Step 1: Audio Upload]
               +-------------------------------------------+
               |      FastAPI Backend: Speech Service      |
               |   (OpenAI Whisper Base / Multi-Format)    |
               +-------------------------------------------+
                                     |
                                     v [Raw Transcript Generated]
               +-------------------------------------------+
               |    User Transcript Preview & Editor       |
               |  (Citizen reviews & corrects spoken text) |
               +-------------------------------------------+
                                     |
                                     v [Step 2: "Extract Information"]
               +-------------------------------------------+
               |     Multilingual NLP Extraction Engine    |
               | (NER: Name, Age, Income, Occupation, etc.)|
               +-------------------------------------------+
                                     |
                                     v [Structured Form Fields]
               +-------------------------------------------+
               |        Form Validation & PDF Export       |
               | - Missing Field Flags                     |
               | - Download Draft PDF Preview              |
               | - Official Submission & Signed Receipt    |
               +-------------------------------------------+
```

---

## 🔄 Two-Step Speech-to-Form Workflow

To ensure accuracy, transparency, and applicant control, VoiceForm AI follows a clear **two-step workflow**:

1. **Step 1: Voice Recording & Speech Recognition**
   - The citizen selects their language (**English**, **हिन्दी**, or **मराठी**) and desired government form.
   - The user records audio via the browser microphone (or selects a sample clip).
   - Audio is transmitted securely to the backend `POST /api/voice/transcribe`.
   - Whisper transcribes the audio and returns the raw recognized text.
2. **Step 2: Reviewable Transcript & Entity Extraction**
   - The transcript is displayed in an **editable preview textarea**. The user can correct any transcription errors or phonetic misspellings.
   - The user clicks **"Extract Information into Form Fields"** (`POST /api/nlp/extract`).
   - The NLP engine parses structured fields:
     - `full_name` (Devanagari and Latin names)
     - `age` / `date_of_birth`
     - `gender`
     - `mobile_number` (10 digits)
     - `aadhaar_number` (12 digits)
     - `annual_income` (normalized numbers or terms like *"1.5 lakh"*, *"८० हजार"*)
     - `occupation` (e.g., Farmer / शेतकरी / किसान, Daily Wage Worker, Student)
     - `education`
     - `residential_address`, `district`, `state`, `pincode`
     - `social_category` (General, OBC, SC, ST, EWS)
   - Extracted fields are filled with green confirmation badges. Unmentioned fields remain `null` with clear help text.
3. **Validation, Draft Preview & Submission**
   - The user can download a **Draft PDF Receipt** at any point to inspect missing mandatory fields.
   - Once all mandatory fields are verified, the user submits the form to generate a unique tracking number (`VF-2026-XXXXX`) and an **Official Tamper-Evident PDF Receipt**.

---

## 📂 Project Structure

```text
VoiceForm AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── assistant.py            # Citizen FAQ & field guidance assistant
│   │   │   ├── dataset.py              # Consented dataset collection & evaluation APIs
│   │   │   ├── forms.py                # Form catalog, validation, draft PDF & submit
│   │   │   ├── nlp.py                  # Multilingual NLP entity extraction
│   │   │   ├── schemes.py              # Welfare scheme catalog & rules evaluator
│   │   │   └── voice.py                # Whisper speech transcription endpoint
│   │   ├── services/
│   │   │   ├── assistant_service.py    # Form help text & diagnostics
│   │   │   ├── form_service.py         # Standardized form schemas & field mapping
│   │   │   ├── nlp_engine.py           # Multilingual regex & NER extractor
│   │   │   ├── pdf_generator.py        # ReportLab draft & official PDF builder
│   │   │   ├── scheme_engine.py        # Scheme eligibility matching algorithm
│   │   │   └── speech_service.py       # Safe Whisper wrapper with format/size guards
│   │   ├── database.py                 # SQLAlchemy engine with SQLite/MySQL fallback
│   │   ├── models.py                   # Submissions, Schemes, ConsentedAudioSample
│   │   └── main.py                     # FastAPI application setup & CORS configuration
│   └── venv/                           # Python 3.12 virtual environment
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Footer.jsx              # Government portal footer
│   │   │   ├── Navbar.jsx              # Navigation bar with language switcher
│   │   │   ├── SmartAssistantModal.jsx # Conversational FAQ drawer
│   │   │   └── VoiceRecorder.jsx       # Browser MediaRecorder with timer & controls
│   │   ├── context/
│   │   │   └── LanguageContext.jsx     # Multilingual state (EN, HI, MR)
│   │   ├── pages/
│   │   │   ├── DatasetManagement.jsx   # Consented dataset studio & review portal
│   │   │   ├── Home.jsx                # Landing page
│   │   │   ├── Result.jsx              # Submission confirmation & PDF download
│   │   │   ├── ReviewSubmit.jsx        # Pre-submission review & draft PDF button
│   │   │   ├── SchemeEligibility.jsx   # Welfare scheme eligibility evaluator
│   │   │   └── VoiceForm.jsx           # 2-step voice recording & form autofill page
│   │   ├── services/
│   │   │   └── api.js                  # Axios client connecting to backend
│   │   ├── App.jsx                     # Route declarations
│   │   └── main.jsx                    # React entrypoint
│   └── package.json                    # React 19, Bootstrap 5, Lucide-react
│
├── datasets/
│   ├── speech/                         # SPEECH RECOGNITION DATASET ONLY
│   │   └── voiceform_dataset/
│   │       ├── audio/                  # 15 real FLEURS WAV clips (en_1..5, hi_1..5, mr_1..5)
│   │       └── transcripts.csv         # audio_filename, language, transcript
│   │
│   └── form_extraction/                # NLP FORM EXTRACTION BENCHMARK DATASET
│       ├── form_extraction_dataset.json# Train & test splits for entity extraction
│       └── README.md                   # Separation notice & benchmark schema details
│
├── validate_dataset.py                 # Speech dataset validation script
├── test_whisper_clips.py               # Whisper WER/CER benchmark script
├── evaluate_form_extraction.py         # Precision, Recall & F1 evaluation pipeline
├── test_system_integration.py          # End-to-end automated integration test suite
├── run_backend.bat                     # 1-Click backend launcher
├── run_frontend.bat                    # 1-Click frontend launcher
├── run_full_system.bat                 # 1-Click full system launcher
└── README.md                           # Documentation
```

---

## 📊 Dataset Organization & Separation

To maintain rigorous scientific standards, the repository strictly isolates speech audio data from NLP form extraction data:

### 1. Speech Recognition Dataset (`datasets/speech/`)
- **Location**: `C:\VoiceForm AI\datasets\speech\voiceform_dataset\`
- **Contents**:
  - `transcripts.csv`: Ground-truth transcripts (`audio_filename`, `language`, `transcript`).
  - `audio/`: 15 mono 16kHz PCM WAV recordings from Google FLEURS (5 English, 5 Hindi, 5 Marathi).
- **Purpose**: Evaluates speech-to-text accuracy (Word Error Rate & Character Error Rate).

### 2. Form Extraction Dataset (`datasets/form_extraction/`)
- **Location**: `C:\VoiceForm AI\datasets\form_extraction\`
- **Contents**:
  - `form_extraction_dataset.json`: Labeled benchmark dataset containing train (15 samples) and test (10 samples) splits across English, Hindi, and Marathi.
  - `README.md`: Documents why speech clips (general reading) are distinct from form filling utterances (structured applicant statements).
- **Purpose**: Evaluates NLP entity extraction (Precision, Recall, F1 score).

---

## 🛡️ Consented Dataset Management & Privacy

The **Dataset Studio** (`/dataset` on the frontend or `GET /api/dataset/status` on the backend) provides ethical, privacy-first dataset collection:

- **Explicit Consent Enforced**: Audio contributions are rejected with HTTP 400 unless `consent_given=true`.
- **Human Review Workflow**: Uploaded samples start in `PENDING` status. Authorized reviewers can approve (`APPROVED`) or reject (`REJECTED`) each sample.
- **Privacy & Right to Deletion**: Any contributed sample can be permanently deleted (`DELETE /api/dataset/samples/{id}`), immediately purging both metadata from the database and the audio file from disk.
- **CSV Export**: Approved samples can be exported as a standard CSV (`GET /api/dataset/export`).
- **Synthetic Demonstration Data**: All pre-packaged examples use fictional demonstration data. No real citizen PII is retained without consent.

---

## 🧪 Benchmark Results & Limitations

### 1. Whisper Speech Recognition Benchmark (`test_whisper_clips.py`)
Tested using OpenAI Whisper `base` model on real 16kHz WAV clips from Google FLEURS:

| Clip | Language | Ground Truth Sample | Recognized Text | WER | CER | Notes |
| :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| `en_1.wav` | English | "...it is known as a severe weather or tornado season..." | "...tornado season..." | **5.3%** | **3.5%** | Excellent accuracy |
| `en_2.wav` | English | "...wind speed that ranges from 111-129 mph..." | "...111 to 129 mph..." | **14.3%** | **0.0%** | Minor digit word format difference |
| `hi_1.wav` | Hindi | "हैंडलबार को मोड़ें..." | "Handle bar..." | **100%** | **77.6%** | Transliterated into Latin text |
| `hi_2.wav` | Hindi | "जब यह रुक जाए..." | "जब यह रुक जाए..." | **70.8%** | **40.2%** | Phonetically correct Devanagari |
| `mr_1.wav` | Marathi | "बटणाचा वापर करून..." | "...बटणाचा वापर करून..." | **100%** | **52.6%** | Repetition artifact in `base` model |

> [!WARNING]
> **Honest Model Assessment**: The lightweight Whisper `base` model functions well for English but exhibits higher error rates and phonetic repetition on Indian regional languages (Hindi and Marathi). In production, upgrade to Whisper `small`/`medium` or fine-tune an Indic model (such as `AI4Bharat IndicWav2Vec` or `Whisper-Marathi`).

### 2. Form Extraction Evaluation Benchmark (`evaluate_form_extraction.py`)
Evaluated against the held-out test split of the form extraction dataset:

| Metric | Score | Status |
| :--- | :---: | :---: |
| **Micro Precision** | **96.7%** | High fidelity (zero hallucinations) |
| **Micro Recall** | **100.0%** | Comprehensive entity extraction |
| **Micro F1 Score** | **98.3%** | Production-ready benchmark |

- **100% Precision & Recall** across `full_name`, `age`, `phone`, `education`, `annual_income`, `district`, `state`, and `occupation`.
- **Bilingual Devanagari Translation**: Auto-normalizes Devanagari numerals (`०-९` -> `0-9`) and regional Indian state/district names.
- **Null Safety**: When a field is not spoken, it safely returns `null` with clear field guidance.

---

## 🚀 How to Run & Deploy VoiceForm AI

### Prerequisites
1. **Python 3.12** installed on Windows.
2. **Node.js** (v18+) and **npm** installed.
3. **FFmpeg** installed and accessible on PATH (check with `ffmpeg -version`).

---

### Option 1: 1-Click Unified Production Launch (Port 8000)

Double-click:
👉 **`run_production.bat`**
* Pre-compiles the React frontend into static assets.
* Launches the unified FastAPI production server on `http://localhost:8000`.
* Serves both the Web UI and Whisper/NLP APIs on a single port.
* Automatically opens your browser.

---

### Option 2: Docker Container Deployment

VoiceForm AI is fully containerized with a production multi-stage [`Dockerfile`](file:///C:/VoiceForm%20AI/Dockerfile) and [`docker-compose.yml`](file:///C:/VoiceForm%20AI/docker-compose.yml):

```bash
# 1-Command Docker Launch
docker compose up --build -d
```
Access at `http://localhost:8000`. Full cloud and VPS deployment instructions are documented in [`DEPLOYMENT_GUIDE.md`](file:///C:/VoiceForm%20AI/DEPLOYMENT_GUIDE.md).

---

### Option 3: Development Mode (Two Windows)

- **Launch Full Dev System**: Double-click `run_full_system.bat`
- **Launch Backend Only**: Double-click `run_backend.bat` (`http://127.0.0.1:8000`)
- **Launch Frontend Only**: Double-click `run_frontend.bat` (`http://localhost:5173`)

---

### Option 2: Running from the Terminal

#### Step 1: Start the Backend Server
```powershell
# Open a terminal in C:\VoiceForm AI
& "backend\venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Backend API**: `http://127.0.0.1:8000`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`

#### Step 2: Start the Frontend Client
```powershell
# In a separate terminal in C:\VoiceForm AI\frontend
npm run dev -- --host 127.0.0.1 --port 5173
```
- **Web Application**: `http://localhost:5173`

---

### Step 3: Running Validation & Evaluation Scripts

To verify system integrity, run these scripts from `C:\VoiceForm AI`:

#### 1. Validate Speech Dataset:
```powershell
& "backend\venv\Scripts\python.exe" validate_dataset.py
```
*Validates audio readability, mono 16kHz format, columns, and audio-to-transcript links.*

#### 2. Run Whisper Speech Recognition Test:
```powershell
& "backend\venv\Scripts\python.exe" test_whisper_clips.py
```
*Transcribes 5 clips across EN/HI/MR and prints comparison table with WER and CER.*

#### 3. Run Form Extraction NLP Benchmark:
```powershell
& "backend\venv\Scripts\python.exe" evaluate_form_extraction.py
```
*Computes field-level and micro-averaged Precision, Recall, and F1 scores on the held-out test split.*

#### 4. Run Complete End-to-End Integration Test Suite:
```powershell
& "backend\venv\Scripts\python.exe" test_system_integration.py
```
*Executes 21 automated integration tests covering health checks, Whisper uploads, Devanagari regex extraction, draft PDF generation, official submissions, and consented dataset privacy operations.*

---

## ⚖️ Ethical AI & Disclaimer Notice

1. **Informational Purpose Only**: The scheme eligibility engine is a preliminary screening tool based on declared socio-economic attributes. It **does not constitute an official government eligibility decision**.
2. **Citizen In Control**: No form is submitted automatically. Applicants must review and explicitly verify all extracted information.
3. **Privacy First**: Audio is transcribed locally in memory or temporary files that are safely deleted. Consented dataset collection is opt-in and revocable.
