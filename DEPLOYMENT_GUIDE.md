# 🚀 VoiceForm AI — Deployment Guide

This guide details how to deploy **VoiceForm AI** across multiple environments: from local single-port production to Docker containers and cloud hosting platforms (Render, Railway, Hugging Face, AWS/Ubuntu).

---

## 🏗️ Deployment Architecture

In production, VoiceForm AI operates as a **unified single-service architecture**:
1. The React 19 frontend is pre-compiled into static HTML/JS/CSS assets inside `frontend/dist/`.
2. The FastAPI backend serves:
   - All REST API endpoints under `/api/*`.
   - The compiled React user interface for web browser requests on `/` and SPA client-side routes (`/forms`, `/schemes`, `/review`, `/result`, `/dataset`).
   - Dynamic port binding via the `PORT` environment variable.

This means **you only need to host and expose a single port (8000)**!

```text
  Internet / User Browser
           │
           ▼ (HTTP Port 8000 / $PORT)
  ┌────────────────────────────────────────────────────────┐
  │              FastAPI Unified Server                    │
  │                                                        │
  │  ├── Web Requests (text/html) ──> Serves frontend/dist │
  │  ├── /assets/*               ──> Static JS & CSS      │
  │  ├── /api/voice/*            ──> Whisper STT Service  │
  │  ├── /api/nlp/*              ──> NER Entity Extractor │
  │  ├── /api/forms/*            ──> Forms & PDF Builder  │
  │  ├── /api/schemes/*          ──> Welfare Scheme Match │
  │  └── /api/dataset/*          ──> Consented Studio     │
  └────────────────────────────────────────────────────────┘
```

---

## ⚡ Option 1: 1-Click Local Production Server (Windows)

To run the application in production mode without needing a separate Vite node process:

1. Double-click:
   👉 **`run_production.bat`**
2. The script:
   - Verifies the frontend production build in `frontend/dist` (running `npm run build` if missing).
   - Starts the unified FastAPI production server on `http://localhost:8000`.
   - Automatically opens your default web browser to `http://localhost:8000`.

---

## 🐳 Option 2: Docker Container Deployment

The project includes a production-grade multi-stage `Dockerfile` and `docker-compose.yml`.

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on Windows, Mac, or Linux.

### Run with Docker Compose
From `C:\VoiceForm AI`:
```bash
docker compose up --build -d
```

* **Application URL**: `http://localhost:8000`
* **API Documentation**: `http://localhost:8000/docs`

To stop the container:
```bash
docker compose down
```

### Manual Docker Build & Run
```bash
# 1. Build the Docker image
docker build -t voiceform-ai:latest .

# 2. Run the container
docker run -d -p 8000:8000 --name voiceform_app voiceform-ai:latest
```

---

## ☁️ Option 3: Free Cloud Deployment (Render.com)

Render.com provides free and straightforward hosting for Docker-based web services.

### Steps:
1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Deploy VoiceForm AI"
   git remote add origin https://github.com/your-username/VoiceForm-AI.git
   git push -u origin main
   ```
2. **Create a Service on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com) and log in.
   - Click **New +** → **Web Service**.
   - Connect your GitHub repository.
   - Select **Docker** as the Environment.
   - Set the instance type (Free or Standard with at least 1GB RAM for Whisper).
   - Click **Deploy Web Service**!
3. Render will automatically build the multi-stage Docker image and provide a live public HTTPS URL (e.g. `https://voiceform-ai.onrender.com`).

*(Note: The pre-configured [`render.yaml`](file:///C:/VoiceForm%20AI/render.yaml) is ready for Render Blueprints).*

---

## 🚂 Option 4: Cloud Deployment on Railway

1. Install the Railway CLI or visit [railway.app](https://railway.app).
2. Connect your GitHub repository.
3. Railway automatically detects the root [`Dockerfile`](file:///C:/VoiceForm%20AI/Dockerfile) and [`Procfile`](file:///C:/VoiceForm%20AI/Procfile).
4. Add environment variables if desired (e.g. `PORT=8000`).
5. Click **Deploy**. Railway will provision an HTTPS domain for your app.

---

## 🖥️ Option 5: Ubuntu Linux VPS / AWS EC2 Deployment

### 1. Install System Dependencies:
```bash
sudo apt update && sudo apt install -y python3.12 python3.12-venv ffmpeg nodejs npm git
```

### 2. Clone Repository & Build Frontend:
```bash
git clone https://github.com/your-username/VoiceForm-AI.git /var/www/voiceform
cd /var/www/voiceform/frontend
npm install
npm run build
```

### 3. Setup Python Backend Environment:
```bash
cd /var/www/voiceform/backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Create Systemd Service:
Create `/etc/systemd/system/voiceform.service`:
```ini
[Unit]
Description=VoiceForm AI Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/voiceform/backend
ExecStart=/var/www/voiceform/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now voiceform
```

---

## 🔒 Production Best Practices Checklist

- [x] **Single Port Unified Hosting**: Frontend and API served from the same origin to eliminate CORS issues in production.
- [x] **Safe Whisper Execution**: Memory bounded with 25MB audio limit and background worker threads.
- [x] **Devanagari Normalization**: Hindi & Marathi numeral translation active.
- [x] **Microphone Fallback**: Live audio level visualizer with WebRTC constraints and manual sample fallback.
