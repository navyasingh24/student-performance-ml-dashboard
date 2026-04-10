# 🎓 Student Performance Prediction Using Ensemble Machine Learning with an Interactive Analytics Dashboard

An end-to-end Machine Learning + Web Application that predicts student grades using multiple models and visualizes results through a modern analytics dashboard.

---

## Features

- Multiple ML Models (KNN, Random Forest, Gradient Boosting, AdaBoost, Extra Trees)
- Interactive Dashboard (Charts + Confidence Meter)
- Grade Prediction (A–F classification)
- Model Comparison & Majority Voting
- Flask Backend API
- Dark-themed modern UI

---

## Dataset

- Source: https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
- 1000 student records
- Features:
  - Gender
  - Ethnicity/Race
  - Parental Education
  - Lunch Type
  - Test Preparation
  - Math, Reading, Writing Scores

---

## Models Used

- K-Nearest Neighbors (KNN)
- Random Forest
- Gradient Boosting (Best Performer)
- AdaBoost
- Extra Trees

---

## 📈 Model Performance

| Model              | Accuracy |
|------------------|---------|
| KNN              | 0.8650  |
| Random Forest    | 0.9350  |
| Gradient Boosting| 0.9400  |
| AdaBoost         | 0.8450  |
| Extra Trees      | 0.9100  |

---

## ⚙️ Tech Stack

- Python (Scikit-learn, Pandas, NumPy)
- Flask (Backend API)
- HTML, CSS, JavaScript
- Chart.js (Data Visualization)

---

## 🖥️ How to Run Locally

```bash
git clone https://github.com/navyasingh24/student-performance-ml-dashboard.git
cd student-performance-ml-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python3 app.py
