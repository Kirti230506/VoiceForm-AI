# 📋 VoiceForm AI — Form Extraction Dataset

## Overview & Separation of Datasets

In VoiceForm AI, **Speech Recognition** and **Form Information Extraction** are maintained as **two distinct datasets**:

1. **Speech Recognition Dataset (`datasets/speech/`)**:
   - Audio recordings (`.wav`) paired with raw verbatim transcripts.
   - Primarily used to evaluate and benchmark Automatic Speech Recognition (ASR) / Whisper accuracy (WER and CER).
   - Contains FLEURS multilingual benchmark audio samples and consented voice recordings.

2. **Form Information Extraction Dataset (`datasets/form_extraction/`)**:
   - Transcribed citizen statements paired with **structured, verified ground-truth form fields**.
   - Used to evaluate Named Entity Recognition (NER), regex parsing, and NLP extraction accuracy (Precision, Recall, F1 score).
   - Does **not** treat ordinary conversational speech transcripts as labeled government forms.

---

## Form Extraction Schema

Each sample in `form_extraction_dataset.json` adheres to this schema:

```json
{
  "id": "FX-001",
  "language": "en", 
  "source_type": "synthetic_demonstration",
  "text": "My name is Ramesh Kumar. I am 42 years old. My mobile number is 9876543210 and Aadhaar is 5432 8765 1290. I am a farmer living in Pune, Maharashtra. My annual income is 1.5 lakh rupees and category is OBC.",
  "target_form": "pm_kisan",
  "ground_truth": {
    "full_name": "Ramesh Kumar",
    "age": 42,
    "date_of_birth": null,
    "gender": "Male",
    "education": null,
    "phone": "9876543210",
    "aadhaar": "5432 8765 1290",
    "occupation": "Farmer / Shetkari / Kisan",
    "annual_income": 150000,
    "district": "Pune",
    "state": "Maharashtra",
    "social_category": "OBC (Other Backward Class)"
  },
  "review_status": "VERIFIED",
  "split": "train"
}
```

---

## Evaluation Guidelines

- Fields not present in the input text **must be labeled as `null`**.
- Evaluator compares predicted extracted values against ground truth for:
  - Exact match (for numbers, phone, Aadhaar, gender)
  - Normalized substring/categorical match (for name, occupation, state, district, category)
- Computes:
  - **Precision**: \( \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}} \)
  - **Recall**: \( \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}} \)
  - **F1 Score**: \( \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \)
