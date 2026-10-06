# 🏠 AI Real Estate Intelligence Platform

An AI-powered real estate platform that combines **Machine Learning, Data Analysis, Generative AI, RAG, FastAPI, and an interactive web interface** to provide intelligent property insights.

> **Built by Hania Eman**
> AI & Data Science Student | ML Developer | Python Enthusiast

---

## ✨ Project Overview

**AI Real Estate Intelligence** is a smart real estate application designed to help users analyze properties, estimate property prices, discover suitable properties, and interact with an AI-powered real estate assistant.

The platform combines traditional Machine Learning with Generative AI and Retrieval-Augmented Generation (RAG) to create a complete AI-based real estate solution.

---

## 🚀 Key Features

### 🧠 ML Price Prediction

Predicts estimated property prices using a trained **Random Forest Regression** model.

* Property quality
* Living area
* Year built
* Basement area
* Garage capacity
* Bathrooms
* Bedrooms
* Lot area
* Neighborhood

### 🏡 Smart Property Recommendations

Finds properties according to user preferences such as:

* 💰 Budget
* 📍 Neighborhood
* 🛏️ Bedrooms
* 📐 Minimum living area
* ⭐ Property quality

The system also provides reasons explaining why a property was recommended.

### 🤖 AI Real Estate Assistant

A Generative AI assistant that can help users with:

* Property-related questions
* Real estate concepts
* Market-related questions
* Property buying guidance
* Investment-related questions

### 📚 RAG Knowledge Assistant

Uses a document-based knowledge base containing real estate information such as:

* Property buying guides
* Investment basics
* Real estate knowledge

The system retrieves relevant information from the knowledge base before providing an answer.

### 📊 Market Insights

Provides dataset-based insights including:

* Average property price
* Median property price
* Price range
* Average living area
* Average property quality
* Neighborhood comparisons
* Property trends

### 🗺️ Interactive Property Map

Interactive map interface using **Leaflet.js** and OpenStreetMap to provide a visual real estate exploration experience.

### 💾 Saved Properties

Users can save interesting properties and manage their saved property list directly from the interface.

### 🌙 Dark Mode

Professional light and dark interface modes for a better user experience.

---

## 🛠️ Technology Stack

| Category         | Technologies               |
| ---------------- | -------------------------- |
| Programming      | Python                     |
| Data Analysis    | Pandas, NumPy              |
| Visualization    | Matplotlib, Seaborn        |
| Machine Learning | Scikit-learn               |
| ML Model         | Random Forest Regressor    |
| Backend          | FastAPI                    |
| Generative AI    | Groq API                   |
| RAG              | TF-IDF Retrieval           |
| Frontend         | HTML, CSS, JavaScript      |
| Interactive Map  | Leaflet.js + OpenStreetMap |
| Model Storage    | Joblib                     |
| Environment      | Python Virtual Environment |
| Version Control  | Git & GitHub               |

---

## 📂 Project Structure

```text
AI-Real-Estate-Intelligence/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── prediction.py
│   │   ├── recommendation.py
│   │   ├── chatbot.py
│   │   ├── rag.py
│   │   └── market.py
│   │
│   ├── services/
│   │   ├── prediction_service.py
│   │   ├── recommendation_service.py
│   │   ├── ai_service.py
│   │   └── rag_service.py
│   │
│   └── schemas/
│       └── property_schema.py
│
├── data/
│   ├── train.csv
│   ├── test.csv
│   ├── sample_submission.csv
│   └── data_description.txt
│
├── documents/
│   ├── real_estate_buying_guide.txt
│   └── property_investment_basics.txt
│
├── ml/
│   ├── data_analysis.py
│   └── evaluate_model.py
│
├── models/
│   └── price_model.joblib
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📈 Machine Learning Pipeline

```text
Real Estate Dataset
        ↓
Data Cleaning & Preprocessing
        ↓
Feature Selection
        ↓
Categorical Encoding
        ↓
Missing Value Handling
        ↓
Random Forest Regression
        ↓
Model Evaluation
        ↓
Saved ML Model
        ↓
FastAPI Prediction API
        ↓
Web Interface
```

---

## 📊 Dataset

This project uses the **Ames Housing Dataset**, containing residential property information and historical sale prices.

Important features include:

* `OverallQual`
* `GrLivArea`
* `YearBuilt`
* `TotalBsmtSF`
* `GarageCars`
* `FullBath`
* `BedroomAbvGr`
* `LotArea`
* `Neighborhood`
* `SalePrice`

The dataset is used for machine learning, property analysis, recommendations, and market insights.

---

## 🔌 API Features

FastAPI provides dedicated endpoints for the major platform services.

```text
/api/health
/api/prediction
/api/recommendation
/api/chatbot
/api/rag
/api/market
```

Interactive API documentation is available through:

```text
/docs
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/haniaeman2026-pixel/AI-Real-Estate-Intelligence.git
cd AI-Real-Estate-Intelligence
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

Windows:

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
GROQ_MODEL=openai/gpt-oss-20b
```

> **Never upload `.env` or API keys to GitHub.**

### 6. Run the application

```bash
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🖥️ Application Modules

The web application provides a unified interface for:

**Dashboard → Price Prediction → Smart Recommendations → AI Assistant → RAG Knowledge Base → Market Insights → Interactive Map → Saved Properties → Settings**

---

## 🎯 Project Objective

The objective of this project is to demonstrate how multiple AI and software engineering technologies can be integrated into a practical real-world application.

Instead of building only an ML model, this project combines:

**Data Analysis + Machine Learning + Generative AI + RAG + FastAPI + Web Development**

into a single intelligent real estate platform.

---

## 🔮 Future Improvements

Planned improvements include:

* Real-time property listings
* Location-based property search
* Geocoded property coordinates
* Advanced market forecasting
* More sophisticated recommendation models
* Vector database-based RAG
* User authentication
* Property comparison
* Personalized investment analysis
* Cloud deployment

---

## 👩‍💻 Developer

**Hania Eman**

AI & Data Science Student
ML Developer | Python Enthusiast

---

## 📌 Project Status

**Version:** 1.0.0
**Status:** Initial Submission / Working Prototype

The platform is continuously being improved with additional UI, AI, recommendation, mapping, and real-world intelligence features.

---

⭐ **If you find this project interesting, consider giving the repository a star!**
