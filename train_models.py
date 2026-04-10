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

# ================= EDA =================
print("\n" + "="*50)
print("📊 EXPLORATORY DATA ANALYSIS")
print("="*50)

# Basic statistics
print("\n📌 Descriptive Statistics:")
print(df.describe())

# Value counts for categorical columns
cat_cols_raw = ['gender', 'race/ethnicity', 'parental level of education',
                'lunch', 'test preparation course']
print("\n📌 Categorical Column Distributions:")
for col in cat_cols_raw:
    print(f"\n{col}:\n{df[col].value_counts()}")

# Score distributions
print("\n📌 Score Distributions (Histograms):")
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
score_cols = ['math score', 'reading score', 'writing score']
for i, col in enumerate(score_cols):
    axes[i].hist(df[col], bins=20, color='steelblue', edgecolor='black')
    axes[i].set_title(f'Distribution of {col}')
    axes[i].set_xlabel('Score')
    axes[i].set_ylabel('Frequency')
plt.tight_layout()
plt.savefig('student_models/score_distributions.png')
plt.show()

# Correlation heatmap
print("\n📌 Correlation Heatmap:")
plt.figure(figsize=(8, 5))
sns.heatmap(df[score_cols].corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.title("Correlation Heatmap - Score Columns")
plt.tight_layout()
plt.savefig('student_models/correlation_heatmap.png')
plt.show()

# Box plots for scores
print("\n📌 Box Plots for Score Columns:")
plt.figure(figsize=(8, 5))
df[score_cols].plot(kind='box', patch_artist=True)
plt.title("Box Plot - Math, Reading, Writing Scores")
plt.tight_layout()
plt.savefig('student_models/boxplots_scores.png')
plt.show()

# Score by gender
print("\n📌 Scores by Gender:")
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, col in enumerate(score_cols):
    df.groupby('gender')[col].mean().plot(kind='bar', ax=axes[i], color=['coral', 'steelblue'])
    axes[i].set_title(f'Avg {col} by Gender')
    axes[i].set_ylabel('Mean Score')
    axes[i].tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig('student_models/scores_by_gender.png')
plt.show()

# Score by test preparation course
print("\n📌 Scores by Test Preparation Course:")
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, col in enumerate(score_cols):
    df.groupby('test preparation course')[col].mean().plot(kind='bar', ax=axes[i], color=['salmon', 'mediumseagreen'])
    axes[i].set_title(f'Avg {col} by Test Prep')
    axes[i].set_ylabel('Mean Score')
    axes[i].tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig('student_models/scores_by_testprep.png')
plt.show()

# Pairplot for score relationships
print("\n📌 Pairplot for Score Columns:")
sns.pairplot(df[score_cols])
plt.suptitle("Pairplot - Score Relationships", y=1.02)
plt.tight_layout()
plt.savefig('student_models/pairplot_scores.png')
plt.show()

# ================= IQR OUTLIER DETECTION =================
print("\n" + "="*50)
print("📌 IQR OUTLIER DETECTION")
print("="*50)

outlier_summary = {}

for col in score_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_summary[col] = {
        'Q1': Q1, 'Q3': Q3, 'IQR': IQR,
        'Lower Bound': lower_bound,
        'Upper Bound': upper_bound,
        'Outlier Count': len(outliers)
    }

    print(f"\n{col}:")
    print(f"  Q1={Q1}, Q3={Q3}, IQR={IQR}")
    print(f"  Lower Bound={lower_bound}, Upper Bound={upper_bound}")
    print(f"  Number of Outliers: {len(outliers)}")
    if len(outliers) > 0:
        print(f"  Outlier Rows:\n{outliers[['math score', 'reading score', 'writing score']].head()}")

# Box plots with outlier highlights
print("\n📌 Box Plots with IQR Outlier Highlights:")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, col in enumerate(score_cols):
    Q1 = outlier_summary[col]['Q1']
    Q3 = outlier_summary[col]['Q3']
    IQR = outlier_summary[col]['IQR']
    lower = outlier_summary[col]['Lower Bound']
    upper = outlier_summary[col]['Upper Bound']

    outliers_mask = (df[col] < lower) | (df[col] > upper)
    axes[i].boxplot(df[col], patch_artist=True,
                    boxprops=dict(facecolor='lightblue'),
                    medianprops=dict(color='red'))
    axes[i].scatter([1] * outliers_mask.sum(),
                    df.loc[outliers_mask, col],
                    color='red', zorder=5, label='Outliers', s=30)
    axes[i].set_title(f'{col}\nOutliers: {outliers_mask.sum()}')
    axes[i].legend()
plt.tight_layout()
plt.savefig('student_models/iqr_outlier_boxplots.png')
plt.show()

print("\n✅ EDA and Outlier Detection complete!")

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