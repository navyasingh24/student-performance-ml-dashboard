# ============================================================
# Student Performance Prediction — Local Training Script
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib, os, json, warnings, time
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_absolute_error)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                              AdaBoostClassifier, ExtraTreesClassifier)

print("✅ All libraries imported successfully!")

# ================= LOAD DATA =================
df = pd.read_csv('StudentsPerformance.csv')

print(f"\n📊 Dataset shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())

# ================= FEATURE ENGINEERING =================
df['avg_score'] = (df['math score'] + df['reading score'] + df['writing score']) / 3

def assign_grade(avg):
    if avg >= 90: return 'A'
    elif avg >= 75: return 'B'
    elif avg >= 60: return 'C'
    elif avg >= 45: return 'D'
    else: return 'F'

df['grade'] = df['avg_score'].apply(assign_grade)
df['pass_fail'] = (df['avg_score'] >= 60).astype(int)

# ================= ENCODING =================
cat_cols = ['gender', 'race/ethnicity', 'parental level of education',
            'lunch', 'test preparation course']

df_encoded = df.copy()
encoders = {}

for col in cat_cols:
    le = LabelEncoder()
    df_encoded[col + '_enc'] = le.fit_transform(df[col])
    encoders[col] = le

le_grade = LabelEncoder()
df_encoded['grade_enc'] = le_grade.fit_transform(df['grade'])

feature_cols = [c + '_enc' for c in cat_cols] + ['math score', 'reading score', 'writing score']
X = df_encoded[feature_cols].values
y = df_encoded['grade_enc'].values

# ================= SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ================= MODELS =================
models = {
    'KNN': KNeighborsClassifier(n_neighbors=7),
    'Random Forest': RandomForestClassifier(n_estimators=200, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=200),
    'AdaBoost': AdaBoostClassifier(n_estimators=150),
    'Extra Trees': ExtraTreesClassifier(n_estimators=200, random_state=42),
}

results = {}
training_times = {}

print("\nTraining models with additional metrics...\n")

for name, model in models.items():
    Xtr = X_train_sc if name == 'KNN' else X_train
    Xte = X_test_sc  if name == 'KNN' else X_test

    start_time = time.time()
    model.fit(Xtr, y_train)
    end_time = time.time()

    training_time = end_time - start_time
    training_times[name] = training_time

    y_pred = model.predict(Xte)
    acc = accuracy_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le_grade.classes_)
    cm = confusion_matrix(y_test, y_pred)

    results[name] = model

    print(f"--- {name} ---")
    print(f"Accuracy: {acc:.4f}")
    print(f"Mean Absolute Error: {mae:.4f}")
    print(f"Training time: {training_time:.2f} seconds")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(cm)
    print("\n")

    # Confusion matrix heatmap
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=le_grade.classes_, yticklabels=le_grade.classes_, cmap="Blues")
    plt.title(f"{name} - Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(f"student_models/{name.lower().replace(' ', '_')}_confusion_matrix.png")
    plt.close()

# ================= SAVE MODELS =================
os.makedirs('student_models', exist_ok=True)

for name, model in results.items():
    fname = name.lower().replace(' ', '_')
    joblib.dump(model, f'student_models/{fname}.pkl')

joblib.dump(scaler, 'student_models/scaler.pkl')
joblib.dump(encoders, 'student_models/encoders.pkl')
joblib.dump(le_grade, 'student_models/label_encoder.pkl')

print("\n✅ Models and scaler/encoders saved successfully!")

# ================= ACCURACY COMPARISON PLOT =================
names = list(results.keys())
accs = []

for name, model in results.items():
    Xte = X_test_sc if name == 'KNN' else X_test
    accs.append(accuracy_score(y_test, model.predict(Xte)))

plt.figure()
plt.bar(names, accs)
plt.xticks(rotation=20)
plt.title("Model Accuracy Comparison")
plt.tight_layout()
plt.savefig("student_models/model_comparison.png")
plt.show()

print("📊 Accuracy comparison plot saved as student_models/model_comparison.png")