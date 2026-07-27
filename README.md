# 🩺 Skin Disease Classification and Stage Identification

## Final Year B.Tech Project

**Department of Computer Science & Engineering**

**United Institute of Technology, Prayagraj**

**Affiliated to Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow**

**Academic Session: 2025–2026**

---

# Abstract

Skin diseases affect millions of people worldwide, and early diagnosis plays a vital role in preventing severe health complications. However, access to experienced dermatologists is limited in many rural and remote areas, resulting in delayed diagnosis and treatment. This project presents an Artificial Intelligence based web application for **Skin Disease Classification and Stage Identification** using Deep Learning.

The proposed system utilizes the **EfficientNetB0** deep learning architecture trained on the **HAM10000** dataset to classify different types of skin diseases. Users can upload a skin image through a Flask-based web application, and the system predicts the disease along with confidence score, risk level, symptoms, disease description, and precautions.

The application is designed to be simple, responsive, and user-friendly, making it suitable for educational purposes and preliminary skin disease screening.

---

# Project Objectives

The primary objectives of this project are:

- To develop an AI-based system for skin disease classification.
- To identify the severity (risk level) of the detected disease.
- To provide confidence score for each prediction.
- To display disease description, symptoms, and precautions.
- To develop a simple and user-friendly web application.
- To assist users in early skin disease screening.
- To improve accessibility of preliminary diagnosis using Artificial Intelligence.

---

# Problem Statement

Skin diseases are among the most common health problems worldwide. Due to the shortage of dermatologists, especially in rural regions, many patients are unable to receive timely diagnosis and treatment.

Traditional diagnosis depends completely on expert medical professionals and manual examination, which is time-consuming and expensive. Therefore, an AI-based automated system can assist users by providing preliminary disease prediction from skin images.

This project addresses this problem by developing a Deep Learning-based web application capable of classifying skin diseases and displaying useful medical information.

---

# Project Features

- AI-Based Skin Disease Classification
- Stage / Risk Level Identification
- Confidence Score
- Upload Skin Image
- Image Preview
- Disease Description
- Symptoms
- Precautions
- Top 3 Predictions
- Secure Image Upload
- Fast Prediction
- Responsive User Interface
- Error Handling
- Flask-Based Web Application

---

# Technologies Used

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- Flask

## Artificial Intelligence / Machine Learning

- TensorFlow
- Keras
- EfficientNetB0
- OpenCV
- NumPy
- Pillow

---

# Software Requirements

- Python 3.10+
- Visual Studio Code
- TensorFlow
- Flask
- OpenCV
- NumPy
- Pillow
- Git
- GitHub

---

# Hardware Requirements

Minimum Requirements

- Intel Core i3 Processor
- 8 GB RAM
- 10 GB Free Storage
- Windows 10 / Windows 11

Recommended

- Intel Core i5 / Ryzen 5
- 16 GB RAM
- SSD Storage
- NVIDIA GPU (Optional)

---

# Dataset Information

Dataset Name

**HAM10000 (Human Against Machine with 10000 Images)**

Image Size

224 × 224 Pixels

Total Classes

7 Skin Disease Classes

Disease Categories

1. Actinic Keratoses (AKIEC)
2. Basal Cell Carcinoma (BCC)
3. Benign Keratosis (BKL)
4. Dermatofibroma (DF)
5. Melanoma (MEL)
6. Melanocytic Nevus (NV)
7. Vascular Lesion (VASC)

---

# Model Information

Model Name

**EfficientNetB0**

Framework

TensorFlow / Keras

Input Size

224 × 224 × 3

Optimizer

Adam

Loss Function

Categorical Crossentropy

Activation Function

Softmax

Transfer Learning

Yes

Output Classes

7

---

# Functional Requirements

- Image Upload
- Image Preprocessing
- Disease Classification
- Risk Level Identification
- Confidence Score Display
- Disease Information Display
- Prediction Result Display

---

# Non Functional Requirements

- High Accuracy
- Fast Response
- User Friendly Interface
- Reliability
- Scalability
- Secure Image Handling
- Easy Accessibility
---

# System Architecture

```
                User
                  │
                  ▼
        Upload Skin Image
                  │
                  ▼
       Image Preprocessing
                  │
                  ▼
      EfficientNetB0 Deep Learning Model
                  │
                  ▼
      Skin Disease Classification
                  │
                  ▼
      Risk Level Identification
                  │
                  ▼
      Result Generation
                  │
                  ▼
Disease Name + Confidence Score
Symptoms + Precautions + Top Predictions
```

---

# Project Workflow

The complete workflow of the system is illustrated below:

1. User uploads a skin disease image.
2. The uploaded image is validated.
3. Image preprocessing is performed.
4. The image is resized to **224 × 224** pixels.
5. The trained EfficientNetB0 model processes the image.
6. The model predicts the disease class.
7. Confidence score is calculated.
8. Risk level is identified.
9. Disease information, symptoms and precautions are displayed.
10. Prediction result is shown to the user.

---

# Project Structure

```
SkinDiseaseClassification/
│
├── app.py
├── config.py
├── train.py
├── model.py
├── predict.py
├── prepare_dataset.py
├── requirements.txt
├── README.md
│
├── models/
│      skin_model.keras
│
├── dataset/
│      train/
│      test/
│
├── static/
│      style.css
│      uploads/
│      js/
│          script.js
│
├── templates/
│      index.html
│      result.html
│      404.html
│      500.html
│
└── utils/
       helper.py
       preprocess.py
```

---

# Installation Guide

## Clone Repository

```bash
git clone <repository-link>
```

## Open Project Folder

```bash
cd SkinDiseaseClassification
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment (Windows)

```bash
venv\Scripts\activate
```

## Install Required Packages

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python app.py
```

## Open Browser

```
http://127.0.0.1:5000
```

---

# Expected Output

The application predicts:

- Disease Name
- Confidence Score
- Risk Level
- Disease Description
- Symptoms
- Precautions
- Top 3 Predictions

---

# Advantages

- Early Skin Disease Detection
- AI-Based Prediction
- User Friendly Interface
- Fast Response Time
- Low Cost Solution
- Easy Accessibility
- Supports Preliminary Diagnosis
- Can be Extended for Mobile Applications

---

# Future Scope

- Increase Number of Disease Classes
- Improve Model Accuracy
- Real Stage Prediction Model
- Grad-CAM Heatmap Visualization
- PDF Report Generation
- Cloud Deployment
- Mobile Application Development
- Doctor Consultation Module
- Patient History Management
- Multi-language Support

---

# Team Members

- **Riya Kesharwani**
- **Deepak Kumar**
- **Rishi Pandey**
- **Shivam Keshri**

---

# Project Supervisor

**Dr. Ankita Srivastava**

Assistant Professor

Department of Computer Science & Engineering

United Institute of Technology

Prayagraj, Uttar Pradesh

---

# References

1. HAM10000 Skin Lesion Dataset
2. TensorFlow Documentation
3. Keras Documentation
4. Flask Documentation
5. EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks
6. OpenCV Documentation

---

# Acknowledgement

We sincerely express our gratitude to **Dr. Ankita Srivastava** for her valuable guidance, continuous encouragement and support throughout the development of this project.

We also thank the **Department of Computer Science & Engineering, United Institute of Technology, Prayagraj**, for providing the necessary facilities and resources to successfully complete this project.

---

# Disclaimer

This project has been developed for **educational and research purposes only**.

The prediction generated by the AI model should **not** be considered a professional medical diagnosis. Users are strongly advised to consult a qualified dermatologist for proper examination and treatment.

---

# License

This project is intended solely for academic use as a Final Year B.Tech Project.

---

# Developed By

**Riya Kesharwani**

**Deepak Kumar**

**Rishi Pandey**

**Shivam Keshri**

Department of Computer Science & Engineering

United Institute of Technology

Prayagraj

Academic Session: **2025–2026**

---

# Thank You

**Skin Disease Classification and Stage Identification**

**Artificial Intelligence for Better Healthcare**