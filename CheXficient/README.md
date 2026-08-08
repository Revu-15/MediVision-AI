# 🫁 CheXficient Chest X-ray Model

This folder contains the Chest X-ray foundation model used by MediVision AI.

---

## Model

**CheXficient**

**Architecture:**

- DINOv2 Image Encoder
- BioClinicalBERT Text Encoder

Used for zero-shot Chest X-ray disease prediction.

---

## Download

Download the model from the official Hugging Face repository:

**[StanfordAIMI/CheXficient on Hugging Face](https://huggingface.co/StanfordAIMI/CheXficient)**

> Click **"Files and versions"** → Download all files

---

## Required Files

Place all downloaded files inside this folder.

**Expected files include:**

```
CheXficient/
├── config.json
├── model.safetensors
├── tokenizer.json
├── tokenizer_config.json
├── processor_config.json
└── README.md
```
