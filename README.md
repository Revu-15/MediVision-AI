# 🏥 MediVision AI

### Intelligent Multi-Modal Medical Diagnosis Platform

Medical Image Analysis • Symptom Diagnosis • AI Medical Reports • Medical Chatbot

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-orange)
![PyTorch](https://img.shields.io/badge/PyTorch-Computer%20Vision-red)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![License](https://img.shields.io/badge/License-MIT-green)


---

# 📖 Overview

MediVision AI is an AI-powered healthcare platform that combines **Computer Vision**, **Deep Learning**, and **Large Language Models (LLMs)** to assist in disease diagnosis from both **medical images** and **patient symptoms**.

The system automatically selects the appropriate AI model based on the uploaded medical image, predicts the disease, generates a professional AI medical report, and allows users to interact with an AI medical chatbot for additional information.

---

# ✨ Features

## 🩻 Medical Image Diagnosis

Supports diagnosis using:

- 🧠 Brain MRI
- 🫁 Chest X-ray
- 👁 Eye Disease
- 🩹 Skin Disease

### Pipeline

```
Medical Image
      │
      ▼
 Florence-2
(Image Captioning)
      │
      ▼
 Image Router
      │
      ▼
 Appropriate AI Model
      │
      ▼
 Disease Prediction
      │
      ▼
 Medical LLM
(Qwen2.5)
      │
      ▼
 Professional Medical Report
```

---

## 🩺 Symptom-Based Diagnosis

Users can enter symptoms instead of uploading an image.

The system predicts

- Disease
- Confidence Score
- AI Reasoning
- Professional Medical Report

---

## 🤖 AI Medical Report

Powered by

**Qwen2.5-0.5B-Instruct**

Generates

- Disease Overview
- Symptoms
- Causes
- Risk Factors
- Complications
- Diagnostic Tests
- Treatment
- Precautions
- Recommended Specialist
- Emergency Warning
- Medical Disclaimer

---

## 💬 Medical Chatbot

Users can ask follow-up questions regarding

- Diseases
- Symptoms
- Reports
- Treatments
- Medical Information

---

# 🧠 AI Models

| Module | Model |
|----------|-------------------------------|
| Image Captioning | Florence-2 |
| Medical LLM | Qwen2.5-0.5B-Instruct |
| Brain MRI | Brain Tumor Classification |
| Chest X-ray | CheXficient |
| Eye Disease | Retinal Disease Classifier |
| Skin Disease | Skin Lesion Classifier |

---

# 📂 Project Structure

```
MediVision_AI/

│
├── BrainMRI/
│     └── README.md
│
├── CheXficient/
│     └── README.md
│
├── EyeDisease/
│     └── README.md
│
├── SkinDisease/
│     └── README.md
│
├── models/
├── routes/
├── templates/
├── static/
├── uploads/
├── reports/
├── utils/
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

# 📥 Model Setup

To keep this repository lightweight, pretrained AI models are **not included** because they exceed GitHub's file size limits.

Each model folder contains a **README.md** explaining where to download the required model.

Download the required models and place them in the following folders:

```
BrainMRI/
CheXficient/
EyeDisease/
SkinDisease/
```

### Models Automatically Downloaded

The following models are automatically downloaded by the application during the first execution.

- Florence-2
- Qwen2.5-0.5B-Instruct

No manual setup is required for these models.

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/Darchol2677/MediVision-AI.git

cd MediVision-AI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Download Required Models

Follow the instructions provided in

```
BrainMRI/README.md
CheXficient/README.md
EyeDisease/README.md
SkinDisease/README.md
```

---

## Run Application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# 🛠 Technology Stack

### Backend

- Flask
- Python

### AI / Deep Learning

- TensorFlow
- PyTorch
- Hugging Face Transformers

### Computer Vision

- OpenCV
- Pillow
- NumPy

### Frontend

- HTML
- CSS
- JavaScript

---

# 🚀 Future Roadmap

- Professional Dashboard
- PDF Report Generation
- User Authentication
- Patient History
- Doctor Dashboard
- Cloud Deployment

---

# ⚠ Disclaimer

This project is intended for educational and research purposes only.

It should not be used as a substitute for professional medical advice, diagnosis, or treatment.

Always consult a qualified healthcare professional.

---

# 👨‍💻 Author

**Yash Satyawan Pawar**

AI • Deep Learning • Computer Vision • Full Stack Development

---

⭐ If you found this project useful, consider giving it a star.
