# 🧠 Multi-Domain Explainable AI Radiology Assistant

A full-stack AI-powered medical imaging system that performs **automatic X-ray type detection, disease diagnosis, explainability visualization, and radiology report generation**.

---

## 🚀 Project Overview

This project is a **Multi-Domain Explainable AI Radiology Assistant** designed to assist in medical image interpretation across multiple radiology domains.

Unlike traditional classifiers, this system provides:

* ✅ Multi-domain diagnosis (Chest, Bone, Dental, Knee)
* ✅ Explainable AI outputs (Grad-CAM & LIME)
* ✅ Severity estimation
* ✅ AI-generated radiology reports

---

## 🎯 Key Features

### 🧠 Intelligent Diagnosis

* Automatic **X-ray type classification**
* Domain-specific disease detection models
* Supports **multi-label predictions**

### 🔍 Explainable AI (XAI)

* Grad-CAM heatmaps for visual attention
* LIME explanations for interpretability

### 📊 Severity Analysis

* Predicts disease severity:

  * Mild
  * Moderate
  * Severe

### 📝 AI Radiology Reports

* Generates structured radiology reports using LLMs:

  * Findings
  * Impression
  * Limitations

### 🌐 Full-Stack Application

* Interactive React frontend
* FastAPI/Flask backend pipeline
* Real-time image analysis

---

## 🏗️ System Architecture

```
User Upload Image
        ↓
Image Type Classifier
        ↓
Domain Routing (Chest / Bone / Dental / Knee)
        ↓
Disease Detection Model
        ↓
Multi-label Prediction
        ↓
Severity Scoring
        ↓
XAI (Grad-CAM + LIME)
        ↓
LLM Report Generation
        ↓
Frontend Visualization
```

---

## 🧱 Core Modules

### 1️⃣ Image Type Classifier

Detects X-ray category:

* Chest
* Bone
* Dental
* Knee

**Model:** MobileNetV2 (Transfer Learning)

---

### 2️⃣ Disease Detection Models

#### 🫁 Chest X-ray

* Pneumonia
* Tuberculosis
* COVID-19
* Pneumothorax
* Pleural Effusion
* Cardiomegaly
* Normal

#### 🦴 Bone X-ray

* Wrist Fracture
* Femur Fracture
* Rib Fracture
* Spine Fracture, etc.
* Normal

#### 😬 Dental X-ray

* Cavity
* Impacted Teeth
* Broken Crown/Root
* Infection
* Normal

#### 🦵 Knee X-ray

* Osteoporosis
* Osteopenia
* Normal

---

### 3️⃣ Multi-Label Classification

* Uses **Sigmoid activation**
* Loss: **Binary Crossentropy**

Example output:

```json
{
  "Pneumonia": 0.82,
  "Effusion": 0.67,
  "Normal": 0.05
}
```

---

### 4️⃣ Severity Scoring

Rule-based severity classification:

| Probability | Severity |
| ----------- | -------- |
| 0.5 – 0.7   | Mild     |
| 0.7 – 0.85  | Moderate |
| > 0.85      | Severe   |

---

### 5️⃣ Explainable AI (XAI)

* **Grad-CAM** → highlights important regions
* **LIME** → local interpretability

---

### 6️⃣ Report Generation (LLM)

Generates radiologist-style reports:

**Input:**

* Disease predictions
* Confidence scores
* Severity

**Output:**

```
Findings:
- Abnormal opacity in lung region

Impression:
- Likely Pneumonia (Moderate)

Limitations:
- Model may misinterpret overlapping tissues
```

---

## 🖥️ Frontend Features

* Image Upload Interface
* Prediction Dashboard
* Probability Charts
* Grad-CAM Visualization
* LIME Explanation Panel
* AI Radiology Report Display

---

## 📁 Project Structure

```
backend/
frontend/
notebooks/
docs/
results/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/rakshitnarang018/x-ai_chest.git
cd xai-medical-imaging
```

---

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

### 3️⃣ Frontend Setup

```bash
cd xai-frontend
npm install
npm start
```

---

## 📥 Models & Dataset

Due to GitHub size limitations, datasets and trained models are not included.


Place models in:

```
backend/saved_models/
```

---

## 📊 Results

* High classification accuracy across domains
* Robust performance on unseen X-ray images
* Explainability improves model trustworthiness

---

## 🧠 Technologies Used

* **Deep Learning:** TensorFlow / Keras
* **Frontend:** React + Tailwind CSS
* **Backend:** Flask / FastAPI
* **XAI:** Grad-CAM, LIME
* **LLM Integration:** OpenAI API
* **Visualization:** Chart.js / Custom UI

---

## ⚠️ Disclaimer

This system is intended for **research and educational purposes only**.
It is **not a substitute for professional medical diagnosis**.

---

## 📌 Future Scope

* Integration with PACS systems
* Real-time clinical deployment
* Multi-modal data fusion (CT, MRI)
* Improved severity prediction models

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share!

---
