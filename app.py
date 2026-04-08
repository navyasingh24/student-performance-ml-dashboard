"""
Student Performance Prediction — Flask Backend
Run:
pip install flask scikit-learn pandas numpy joblib flask-cors

Then:
python app.py
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import os
import numpy as np

app = Flask(__name__)
CORS(app)

# ── Load artefacts ────────────────────────────────────────
BASE = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE, 'student_models')

scaler    = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
encoders  = joblib.load(os.path.join(MODEL_DIR, 'encoders.pkl'))
le_grade  = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.pkl'))

MODEL_FILES = {
    'KNN':               'knn.pkl',
    'Random Forest':     'random_forest.pkl',
    'Gradient Boosting': 'gradient_boosting.pkl',
    'AdaBoost':          'adaboost.pkl',
    'Extra Trees':       'extra_trees.pkl',
}

models = {}
for name, fname in MODEL_FILES.items():
    path = os.path.join(MODEL_DIR, fname)
    if os.path.exists(path):
        models[name] = joblib.load(path)

# ── Feature Columns ───────────────────────────────────────
CAT_COLS = [
    'gender',
    'race/ethnicity',
    'parental level of education',
    'lunch',
    'test preparation course'
]

# ── Encode Input ───────────────────────────────────────────
def encode_input(data: dict) -> np.ndarray:
    row = []

    # categorical encoding
    for col in CAT_COLS:
        val = data.get(col, '')
        le  = encoders[col]

        if val not in le.classes_:
            raise ValueError(f"Invalid value '{val}' for '{col}'")

        row.append(int(le.transform([val])[0]))

    # numerical features
    try:
        row.append(float(data.get('math score')))
        row.append(float(data.get('reading score')))
        row.append(float(data.get('writing score')))
    except:
        raise ValueError("Invalid score values")

    return np.array(row).reshape(1, -1)

# ── Routes ────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    body = request.get_json(force=True)

    try:
        X_raw = encode_input(body)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    X_sc = scaler.transform(X_raw)

    preds = {}

    # ── Model Predictions ──
    for name, model in models.items():
        Xin = X_sc if name == 'KNN' else X_raw
        grade_enc = int(model.predict(Xin)[0])
        grade_lbl = le_grade.inverse_transform([grade_enc])[0]

        preds[name] = grade_lbl

    # ── Majority Voting ──
    grades = list(preds.values())
    majority = max(set(grades), key=grades.count)

    # ── Probabilities (from best model) ──
    probs = {}
    if 'Gradient Boosting' in models and hasattr(models['Gradient Boosting'], 'predict_proba'):
        proba_arr = models['Gradient Boosting'].predict_proba(X_raw)[0]
        probs = {
            le_grade.classes_[i]: float(p)
            for i, p in enumerate(proba_arr)
        }

    # ── Convert model names to frontend keys ──
    model_map = {
        "KNN": "knn",
        "Random Forest": "rf",
        "Gradient Boosting": "gb",
        "AdaBoost": "ada",
        "Extra Trees": "et"
    }

    formatted_preds = {
        model_map[k]: v for k, v in preds.items()
    }

    # ── Final Response (MATCHES FRONTEND) ──
    return jsonify({
        "predicted_grade": majority,
        "majority_vote": majority,
        "model_predictions": formatted_preds,
        "probabilities": probs
    })


@app.route('/api/options', methods=['GET'])
def options():
    return jsonify({
        col: list(map(str, encoders[col].classes_))
        for col in CAT_COLS
    })


# ── Run Server ─────────────────────────────────────────────
if __name__ == '__main__':
    print(f"Loaded models: {list(models.keys())}")
    app.run(debug=True, port=5001)