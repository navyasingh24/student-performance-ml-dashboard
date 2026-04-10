# ============================================================
# Student Performance Prediction — FINAL COMPLETE SCRIPT
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib, os, warnings, time
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_absolute_error)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                              AdaBoostClassifier, ExtraTreesClassifier)

print("✅ All libraries imported successfully!")

# ================= CREATE FOLDER =================
os.makedirs('student_models', exist_ok=True)

# ================= LOAD DATA =================
df = pd.read_csv('StudentsPerformance.csv')

print(f"\n📊 Dataset shape: {df.shape}")
print("\nMissing values:\n", df.isnull().sum())

# ================= EDA =================
print("\n📊 EDA STARTED")

score_cols = ['math score', 'reading score', 'writing score']

# ---- HISTOGRAMS ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, col in enumerate(score_cols):
    axes[i].hist(df[col], bins=20)
    axes[i].set_title(col)
plt.tight_layout()
plt.savefig('student_models/score_distributions.png')
plt.close()

# ---- CORRELATION HEATMAP ----
plt.figure(figsize=(6, 4))
sns.heatmap(df[score_cols].corr(), annot=True)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig('student_models/correlation_heatmap.png')
plt.close()

# ---- BOXPLOTS ----
plt.figure(figsize=(6, 4))
df[score_cols].plot(kind='box')
plt.title("Boxplot of Scores")
plt.tight_layout()
plt.savefig('student_models/boxplots_scores.png')
plt.close()

# ---- PAIRPLOT ----
pairplot = sns.pairplot(df[score_cols])
pairplot.savefig('student_models/pairplot_scores.png')
plt.close()

# ---- GENDER ANALYSIS ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, col in enumerate(score_cols):
    df.groupby('gender')[col].mean().plot(kind='bar', ax=axes[i])
plt.tight_layout()
plt.savefig('student_models/scores_by_gender.png')
plt.close()

# ---- TEST PREP ANALYSIS ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, col in enumerate(score_cols):
    df.groupby('test preparation course')[col].mean().plot(kind='bar', ax=axes[i])
plt.tight_layout()
plt.savefig('student_models/scores_by_testprep.png')
plt.close()

# ================= OUTLIER DETECTION =================
print("\n📊 OUTLIER DETECTION")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, col in enumerate(score_cols):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    axes[i].boxplot(df[col])
    axes[i].scatter([1]*len(outliers), outliers[col])
    axes[i].set_title(f"{col} (Outliers: {len(outliers)})")

plt.tight_layout()
plt.savefig('student_models/iqr_outlier_boxplots.png')
plt.close()

print("✅ EDA DONE")

# ================= FEATURE ENGINEERING =================
df['avg_score'] = df[score_cols].mean(axis=1)

def assign_grade(x):
    if x >= 90: return 'A'
    elif x >= 75: return 'B'
    elif x >= 60: return 'C'
    elif x >= 45: return 'D'
    else: return 'F'

df['grade'] = df['avg_score'].apply(assign_grade)

# ================= ENCODING =================
cat_cols = ['gender', 'race/ethnicity', 'parental level of education',
            'lunch', 'test preparation course']

encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

le_grade = LabelEncoder()
df['grade'] = le_grade.fit_transform(df['grade'])

X = df[cat_cols + score_cols]
y = df['grade']

# ================= SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

# ================= MODELS =================
models = {
    'KNN': KNeighborsClassifier(n_neighbors=7),
    'Random Forest': RandomForestClassifier(n_estimators=200, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=200),
    'AdaBoost': AdaBoostClassifier(n_estimators=150),
    'Extra Trees': ExtraTreesClassifier(n_estimators=200, random_state=42)
}

results = {}
accs = []

print("\n🚀 TRAINING MODELS\n")

for name, model in models.items():
    Xtr = X_train_sc if name == 'KNN' else X_train
    Xte = X_test_sc if name == 'KNN' else X_test

    start = time.time()
    model.fit(Xtr, y_train)
    end = time.time()

    y_pred = model.predict(Xte)

    acc = accuracy_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    accs.append(acc)

    print(f"\n🔥 {name}")
    print(f"Accuracy: {acc:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"Training Time: {end-start:.4f}s")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)

    # ---- SAVE CONFUSION MATRIX PLOT ----
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title(name)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(f'student_models/{name.replace(" ", "_")}_cm.png')
    plt.close()

    results[name] = model
    joblib.dump(model, f'student_models/{name.replace(" ", "_")}.pkl')

# ================= SAVE PREPROCESSING =================
joblib.dump(scaler, 'student_models/scaler.pkl')
joblib.dump(encoders, 'student_models/encoders.pkl')
joblib.dump(le_grade, 'student_models/label_encoder.pkl')

print("\n✅ Models & preprocessors saved!")

# ================= MODEL COMPARISON =================
plt.figure()
plt.bar(results.keys(), accs)
plt.xticks(rotation=20)
plt.title("Model Accuracy Comparison")
plt.tight_layout()
plt.savefig('student_models/model_comparison.png')
plt.close()

print("\n🔥 EVERYTHING DONE & SAVED IN student_models/")