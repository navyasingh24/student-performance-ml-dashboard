"""
Student Performance Prediction — Flask Backend
Run: pip install flask scikit-learn pandas numpy joblib flask-cors
Then: python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, json, os, numpy as np

app = Flask(__name__)
CORS(app)

# ── Load artefacts ────────────────────────────────────────
BASE = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE, 'student_models')

scaler    = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
encoders  = joblib.load(os.path.join(MODEL_DIR, 'encoders.pkl'))
le_grade  = joblib.load(os.path.join(MODEL_DIR, 'label_encoder_grade.pkl'))

MODEL_FILES = {
    'KNN':               'knn_model.pkl',
    'Random Forest':     'random_forest_model.pkl',
    'Gradient Boosting': 'gradient_boosting_model.pkl',
    'AdaBoost':          'adaboost_model.pkl',
    'Extra Trees':       'extra_trees_model.pkl',
}

models = {}
for name, fname in MODEL_FILES.items():
    path = os.path.join(MODEL_DIR, fname)
    if os.path.exists(path):
        models[name] = joblib.load(path)

with open(os.path.join(MODEL_DIR, 'model_metrics.json')) as f:
    MODEL_METRICS = json.load(f)

CAT_COLS = ['gender', 'race/ethnicity', 'parental level of education',
            'lunch', 'test preparation course']

def encode_input(data: dict) -> np.ndarray:
    row = []
    for col in CAT_COLS:
        val = data.get(col, '')
        le  = encoders[col]
        if val not in le.classes_:
            raise ValueError(f"Unknown value '{val}' for '{col}'. "
                             f"Valid: {list(le.classes_)}")
        row.append(int(le.transform([val])[0]))
    return np.array(row).reshape(1, -1)

# ── Routes ────────────────────────────────────────────────

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'models_loaded': list(models.keys())})

@app.route('/api/predict', methods=['POST'])
def predict():
    body = request.get_json(force=True)
    try:
        X_raw = encode_input(body)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    X_sc  = scaler.transform(X_raw)          # for KNN
    preds = {}

    for name, model in models.items():
        Xin = X_sc if name == 'KNN' else X_raw
        grade_enc  = int(model.predict(Xin)[0])
        grade_lbl  = le_grade.inverse_transform([grade_enc])[0]

        proba = None
        if hasattr(model, 'predict_proba'):
            proba_arr = model.predict_proba(Xin)[0]
            proba = {le_grade.classes_[i]: round(float(p), 4)
                     for i, p in enumerate(proba_arr)}

        preds[name] = {
            'grade': grade_lbl,
            'grade_enc': grade_enc,
            'probabilities': proba,
        }

    # Majority vote
    grades = [v['grade'] for v in preds.values()]
    majority = max(set(grades), key=grades.count)

    return jsonify({
        'predictions': preds,
        'majority_vote': majority,
        'input': body,
    })

@app.route('/api/metrics', methods=['GET'])
def metrics():
    return jsonify(MODEL_METRICS)

@app.route('/api/options', methods=['GET'])
def options():
    """Return valid dropdown options for the frontend."""
    return jsonify({
        col: list(map(str, encoders[col].classes_))
        for col in CAT_COLS
    })

if __name__ == '__main__':
    print(f"Loaded models: {list(models.keys())}")
    app.run(debug=True, port=5000)
