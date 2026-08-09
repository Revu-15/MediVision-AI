# 🏥 MediVision AI

### Intelligent Multi-Modal Medical Diagnosis & Report Generation Platform

**Medical Image Analysis • General Clinical Photo Scanning • Symptom AI Diagnosis • Structured Clinical Reports • AI Medical Assistant • PDF Export**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.6.0-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![HuggingFace](https://img.shields.io/badge/Transformers-Florence--2%20%7C%20Qwen2.5-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> 🌐 **Live Application Demo:** [https://devoutly-walnut-cartridge.ngrok-free.dev/](https://devoutly-walnut-cartridge.ngrok-free.dev/)

---

## 📖 Overview

**MediVision AI** is an advanced medical AI system that integrates **Computer Vision**, **Multi-Modal AI Vision-Language Models (Florence-2)**, and **Large Language Models (Qwen2.5-0.5B-Instruct)** to diagnose diseases from medical imaging scans, general medical/skin photographs, or reported patient symptoms.

The system features an automated diagnostic pipeline:
1. **Visual Feature Extraction:** Florence-2 analyzes scan features or dermatological photos.
2. **Specialized Neural Classifier Dispatch:** Automatically routes to Brain MRI, Chest X-ray, Retinal Fundus, or General Medical handlers.
3. **LLM Clinical Report Generation:** Qwen2.5 produces structured clinical reports (Overview, Symptoms, Causes, Complications, Diagnostic Tests, Treatment, Specialist recommendations).
4. **PDF Report Export & Conversational AI:** Export official PDF reports and ask follow-up questions to an interactive AI Medical Assistant.

---

## ✨ Key Features

### 🩻 1. Multi-Modal Medical Image Scan Analysis
- **🧠 Brain MRI Scans:** Detects Glioma, Meningioma, Pituitary tumors, or Normal tissue.
- **🫁 Chest X-rays & Lung Scans:** Analyzes 13 pulmonary conditions (Pneumonia, Tuberculosis, COVID-19, Pleural Effusion, Cardiomegaly, etc.).
- **👁 Retinal / Eye Fundus Scans:** Detects 45 retinal pathologies (Diabetic Retinopathy, Macular Degeneration, Drusen, Glaucoma signs, etc.).
- **🩺 General Medical & Skin Photos:** Visual analysis of skin lesions, rashes, wounds, CT, ultrasound, or general medical photos via **Florence-2 Vision AI**.

---

### 🩺 2. Intelligent Symptom Diagnosis
- Input patient symptoms in plain English.
- Instant AI prediction with confidence scores, clinical reasoning, and differential diagnosis options.
- Optimized response times (< 2 seconds) with reliable fallback parsing.

---

### 📄 3. Clinical Report Generation & PDF Export
- Generates structured medical reports with overview, common symptoms, primary causes, risk factors, complications, diagnostic tests, treatments, and recommended specialists.
- Displays scan image preview alongside AI confidence indicators.
- One-click **PDF Download** styled for clinical documentation.

---

### 💬 4. Interactive Medical AI Chatbot
- Ask follow-up questions about diagnosis, medications, or treatment protocols.
- Grounded directly on patient's scan/symptom report context.

---

## 🏗 Diagnostic Pipeline Architecture

```
                       ┌──────────────────────────┐
                       │  Uploaded Scan / Photo   │
                       └────────────┬─────────────┘
                                    │
                                    ▼
                       ┌──────────────────────────┐
                       │   Florence-2 Vision AI   │
                       │ (Visual Feature Caption) │
                       └────────────┬─────────────┘
                                    │
                                    ▼
                       ┌──────────────────────────┐
                       │    Model Router &        │
                       │     Dispatcher           │
                       └─────┬───┬───┬─────────┬──┘
                             │   │   │         │
       ┌─────────────────────┘   │   └─────┐   └───┐
       ▼                         ▼         ▼       ▼
┌──────────────┐         ┌───────────┐ ┌───────┐ ┌───────────────┐
│  Brain MRI   │         │ Chest Xray│ │Retinal│ │General Medical│
│ Classifier   │         │CheXficient│ │ Scan  │ │ Vision AI     │
└──────┬───────┘         └─────┬─────┘ └───┬───┘ └───────┬───────┘
       │                       │           │             │
       └───────────────────┐   │   ┌───────┘             │
                           ▼   ▼   ▼                     │
                        ┌─────────────┐                  │
                        │ Prediction  │◄─────────────────┘
                        └──────┬──────┘
                               │
                               ▼
                       ┌──────────────────────────┐
                       │ Qwen2.5-0.5B Medical LLM │
                       │(Report & Recommendations)│
                       └────────────┬─────────────┘
                                    │
                                    ▼
                       ┌──────────────────────────┐
                       │ Clinical Report & PDF    │
                       └──────────────────────────┘
```

---

## 🛠 Technology Stack

- **Backend Framework:** Flask 3.1.0, Gunicorn 23.0.0, Python 3.11 / 3.12
- **AI & Computer Vision:** PyTorch 2.6.0, Hugging Face Transformers (`Florence-2-base`, `Qwen2.5-0.5B-Instruct`), Pillow, OpenCV, NumPy, timm, einops
- **PDF Generation:** ReportLab 4.4.1
- **Frontend UI:** HTML5, Modern CSS Design System, JavaScript (Vanilla ES6+), FontAwesome 6

---

## 📂 Project Structure

```
MediVision-AI/
├── app.py                      # Flask Application Server & Routing
├── render.yaml                 # Render Cloud Deployment Config
├── Dockerfile                  # Container Config (Hugging Face / Docker)
├── MediVision_Colab_Deploy.ipynb# Google Colab + ngrok Deployment Notebook
├── requirements.txt            # Python Dependencies
├── .env                        # Environment Configuration
│
├── models/                     # AI Engine & Neural Classifiers
│   ├── shared_models.py        # Model Singleton Loader
│   ├── florence2.py            # Florence-2 Vision AI Captioner
│   ├── medical_llm.py          # Qwen2.5 Medical LLM Engine
│   ├── image_router.py         # Image Classifier Router
│   ├── model_dispatcher.py     # Execution Dispatcher
│   ├── brain_mri_model.py      # Brain Tumor Model Handler
│   ├── chest_xray_model.py     # Chest X-Ray Model Handler
│   ├── eye_disease_model.py    # Retinal Disease Model Handler
│   ├── general_medical_model.py# General & Skin Photo Handler
│   └── ai_report_engine.py     # Report Generation Orchestrator
│
├── routes/                     # Blueprint API Endpoints
│   ├── upload.py               # Image Diagnosis Controller
│   ├── symptoms.py             # Symptom Diagnosis Controller
│   ├── chatbot.py              # AI Chat Controller
│   └── download.py             # PDF Report Download Controller
│
├── BrainMRI/                   # Brain MRI Weights Setup
├── CheXficient/                # Chest X-ray Weights Setup
├── EyeDisease/                 # Retinal Scan Weights Setup
│
├── static/                     # CSS, Images & Sample Scans
│   ├── css/
│   ├── images/
│   └── samples/                # Built-in Test Sample Scans
├── templates/                  # Jinja2 HTML View Templates
│   ├── index.html              # Landing Page
│   ├── dashboard.html          # Clinical Dashboard
│   ├── upload.html             # Image Upload & Scan Module
│   ├── symptoms.html           # Symptom Diagnosis Module
│   ├── report.html             # Clinical Report View
│   ├── chatbot.html            # AI Medical Assistant
│   └── settings.html           # System Settings
├── uploads/                    # Scanned Images Storage
└── reports/                    # Generated JSON & PDF Reports
```

---

## ⚙ Local Installation & Running

### 1. Clone Repository
```bash
git clone https://github.com/Revu-15/MediVision-AI.git
cd MediVision-AI
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=medivision_ai_secret_key_2026
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

### 5. Start the Application
```bash
python app.py
```

Open your browser at:  
👉 **`http://127.0.0.1:5000`**

*(Note: On first startup, Hugging Face models will automatically download).*

---

## 🌐 Deployment Options

### Option 1: FREE Deployment via Google Colab + ngrok (Recommended)

1. Open the included notebook in Google Colab:  
   👉 **[MediVision_Colab_Deploy.ipynb](MediVision_Colab_Deploy.ipynb)**
2. Select **Runtime → Change runtime type → T4 GPU** (for fast GPU inference).
3. Paste your Gemini API key and free ngrok AuthToken.
4. Run all cells — get a public HTTPS URL (`https://xxxx.ngrok-free.app`) to share instantly!

---

### Option 2: Local ngrok Public Tunnel

If running locally on your PC, share your server to the internet in 1 step:

```powershell
# Authenticate ngrok (one-time setup)
.\venv\Scripts\ngrok.exe config add-authtoken YOUR_NGROK_TOKEN

# Share local server
.\venv\Scripts\ngrok.exe http 5000
```

---

### Option 3: Docker / Container Deployment

Build and run using Docker:

```bash
# Build image
docker build -t medivision-ai .

# Run container
docker run -p 7860:7860 -e GOOGLE_API_KEY="YOUR_KEY" medivision-ai
```

---

### Option 4: Deploy on Render / Cloud Platforms

The project includes `render.yaml` preconfigured for cloud deployment:
1. Connect your repository `Revu-15/MediVision-AI` on **Render.com**.
2. Select **Web Service** (Render automatically reads `render.yaml`).
3. Set Environment Variable: `GOOGLE_API_KEY`.
4. Deploy!

---

## ⚠ Disclaimer

*This project is for educational, demonstration, and research purposes only. It is not intended to provide medical advice or replace professional clinical diagnosis. Always consult a licensed medical professional for clinical decisions.*

---

## 👨‍💻 Author & Repository

- **Repository:** [https://github.com/Revu-15/MediVision-AI](https://github.com/Revu-15/MediVision-AI)
- **License:** MIT License

⭐ *If you find MediVision AI helpful, please consider giving the repository a star on GitHub!*
