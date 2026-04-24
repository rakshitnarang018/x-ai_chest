# Backend Setup

## Prerequisites

Install:

* **Python 3.10** (recommended for TensorFlow)
* **Git**
* **Ollama**

Verify:

```bash
python --version
git --version
```

Pull and test model:

```bash
ollama pull phi3
ollama run phi3
```

---

## Clone Project

```bash
git clone <repo-url>
cd x-ai-for-medical-imaging
```

## Required Backend Structure

```bash
backend/
├── app/
├── saved_models/
├── uploads/
├── temp/
├── test_images/
└── requirements.txt
```

## Required Models

Place inside `backend/saved_models/`:

* type_classifier.keras
* chest_final.keras
* bone_final.keras
* knee_final.keras
* dental_final.keras

---

## Setup Virtual Environment

```bash
cd backend
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify:

```bash
python -c "import tensorflow as tf; print(tf.__version__)"
python -c "import cv2; print(cv2.__version__)"
python -c "import lime; print('ok')"
```

Verify models:

```bash
python -c "from app.core.model_registry import ModelRegistry; ModelRegistry.load_models(); print(ModelRegistry.list_models())"
```

---

## Environment Variables

Create `.env`

```env
OLLAMA_URL=http://localhost:11434
```

## Start Ollama

```bash
ollama serve
```

## Run Backend

```bash
uvicorn app.main:app --reload
```

API:

* [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Test API

Health:

```bash
curl http://127.0.0.1:8000/health
```

Analyze:

```bash
curl -X POST -F "file=@test_images/sample.png" http://127.0.0.1:8000/analyze
```

---

## API Endpoints

### 1. Health Check

**GET** `/health`

Response:

```json
{
  "status": "healthy",
  "service": "x-ai-medical-imaging"
}
```

---

### 2. Analyze Image

**POST** `/analyze`

Request:

* Multipart form-data
* Field: `file`

Example:

```bash
curl -X POST -F "file=@test_images/sample.png" http://127.0.0.1:8000/analyze
```

Response:

```json
{
  "job_id": "abc123",
  "status": "processing",
  "message": "Analysis started"
}
```

---

### 3. Get Analysis Result

**GET** `/analysis/{job_id}`

Example:

```bash
curl http://127.0.0.1:8000/analysis/abc123
```

Response:

```json
{
  "job_id": "abc123",
  "status": "completed",
  "scan_type": "chest",
  "prediction": "Pneumonia",
  "confidence": 0.96,
  "explanation": "Model explanation output"
}
```

---

### 4. Generate LIME Explanation

**POST** `/analysis/{job_id}/lime`

Example:

```bash
curl -X POST http://127.0.0.1:8000/analysis/abc123/lime
```

Response:

```json
{
  "job_id": "abc123",
  "lime_generated": true,
  "heatmap_path": "outputs/lime_abc123.png"
}
```

---

## Notes

* Uses attached `requirements.txt` for full dependency installation
* TensorFlow 2.21 + FastAPI + LIME + OpenCV configured
* Ollama (`phi3`) required for AI explanation features
