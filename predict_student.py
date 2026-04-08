import joblib
import numpy as np
import os

# ---------------- Load Models, Encoders, Scaler ----------------
encoders = joblib.load('student_models/encoders.pkl')
scaler = joblib.load('student_models/scaler.pkl')
le_grade = joblib.load('student_models/label_encoder.pkl')

# Load all trained models
model_files = [f for f in os.listdir('student_models') 
               if f.endswith('.pkl') and f not in ['scaler.pkl', 'encoders.pkl', 'label_encoder.pkl']]
models = {f.replace('.pkl','').replace('_',' ').title(): joblib.load(f'student_models/{f}') for f in model_files}

# ---------------- Helper Functions ----------------
def get_valid_input(prompt, encoder_name):
    classes = encoders[encoder_name].classes_
    print(f"Valid options for {prompt}: {list(classes)}")
    while True:
        value = input(f"{prompt}: ").strip()
        if value in classes:
            return value
        print("Invalid input, please enter exactly one of the above.")

def get_numeric_input(prompt):
    while True:
        try:
            return float(input(f"{prompt}: "))
        except ValueError:
            print("Invalid input, enter a number.")

# ---------------- Collect Inputs ----------------
print("Enter student details:")
gender = get_valid_input("Gender (male/female)", 'gender')
race = get_valid_input("Race / Ethnicity (Group A-E)", 'race/ethnicity')
parent_edu = get_valid_input("Parental Level of Education", 'parental level of education')
lunch = get_valid_input("Lunch Type (standard/free/reduced)", 'lunch')
prep_course = get_valid_input("Test Prep Course (completed/none)", 'test preparation course')

math_score = get_numeric_input("Math Score")
reading_score = get_numeric_input("Reading Score")
writing_score = get_numeric_input("Writing Score")

# ---------------- Encode Inputs ----------------
gender_enc = encoders['gender'].transform([gender])[0]
race_enc = encoders['race/ethnicity'].transform([race])[0]
parent_enc = encoders['parental level of education'].transform([parent_edu])[0]
lunch_enc = encoders['lunch'].transform([lunch])[0]
prep_course_enc = encoders['test preparation course'].transform([prep_course])[0]

x_raw = np.array([[gender_enc, race_enc, parent_enc, lunch_enc, prep_course_enc,
                   math_score, reading_score, writing_score]])
x_scaled = scaler.transform(x_raw)

# ---------------- Predict with All Models ----------------
print("\nPredictions from all models (grade categories A-F):")
for name, model in models.items():
    # KNN was trained on scaled data, others on raw
    pred_input = x_scaled if 'Knn' in name else x_raw
    pred_encoded = model.predict(pred_input)[0]
    pred_grade = le_grade.inverse_transform([pred_encoded])[0]
    print(f"{name}: {pred_grade}")

# ---------------- Optional: Final Grade based on Average Score ----------------
avg_score = (math_score + reading_score + writing_score) / 3
if avg_score >= 90: final_grade = 'A'
elif avg_score >= 75: final_grade = 'B'
elif avg_score >= 60: final_grade = 'C'
elif avg_score >= 45: final_grade = 'D'
else: final_grade = 'F'

print(f"\n✅ Final Grade (based on average score): {final_grade}")
