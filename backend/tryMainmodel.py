import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# ---- GET CORRECT FILE PATHS ----
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
csv_path = os.path.join(project_root, "data", "train_with_major.csv")

print(f"Looking for CSV at: {csv_path}")
print(f"File exists: {os.path.exists(csv_path)}")

# ---- LOAD DATASET ----
try:
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded {len(df)} rows from CSV")
    print(f"Columns in dataset: {df.columns.tolist()}")
except FileNotFoundError:
    print(f"ERROR: Could not find file at {csv_path}")
    print(f"Current working directory: {os.getcwd()}")
    exit(1)

# ---- CLEAN COLUMN NAMES (remove extra spaces) ----
df.columns = df.columns.str.strip()

print(f"\nCleaned columns: {df.columns.tolist()}")

# ---- SELECT FEATURES (using actual column names) ----
features = [
    "Rating",              # Programming Languages Rating
    "Rating.1",            # Soft Skills Rating
    "Current Course",
    "Technical Skills",
    "Projects",
    "Challenges"
]

# Check if all features exist
missing_cols = [col for col in features if col not in df.columns]
if missing_cols:
    print(f"\nERROR: Missing columns: {missing_cols}")
    print(f"Available columns: {df.columns.tolist()}")
    exit(1)

X = df[features]
y = df["Career Interest"]

print(f"\n✓ Features selected: {features}")
print(f"✓ Target variable: Career Interest")
print(f"✓ Unique career paths: {y.nunique()}")

# ---- PREPROCESSING PIPELINE ----
numeric_features = ["Rating", "Rating.1"]
categorical_features = ["Current Course", "Technical Skills", "Challenges", "Projects"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough"
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# ---- TRAIN MODEL ----
print("\n" + "="*50)
print("Training model...")
print("="*50)
model.fit(X, y)
print("✓ Model training complete!")

# ---- SAVE MODEL ----
model_path = os.path.join(script_dir, "tryMainmodel.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✓ Model saved successfully at: {model_path}")
print("="*50) 