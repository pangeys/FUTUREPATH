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
csv_path = os.path.join(script_dir, "data", "train_with_major.csv")

print("\n" + "="*70)
print("📁 FILE PATH SETUP")
print("="*70)
print(f"Script directory: {script_dir}")
print(f"Project root:     {project_root}")
print(f"CSV path:         {csv_path}")
print(f"File exists:      {os.path.exists(csv_path)}")
print("="*70 + "\n")

# ---- LOAD DATASET ----
try:
    df = pd.read_csv(csv_path)
    print(f"✓ Successfully loaded {len(df)} rows from CSV")
    print(f"✓ Columns in dataset: {df.columns.tolist()}\n")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find file at {csv_path}")
    print(f"Current working directory: {os.getcwd()}")
    print("\nPlease ensure:")
    print("  1. The 'data' folder exists in 'backend/'")
    print("  2. The file 'train_with_major.csv' is inside 'backend/data/'")
    exit(1)

# ---- CLEAN COLUMN NAMES (remove extra spaces) ----
df.columns = df.columns.str.strip()

print(f"Cleaned columns: {df.columns.tolist()}\n")

# ---- SELECT FEATURES (using actual column names) ----
features = [            
    "Soft Skills Rating",              # Soft Skills Rating
    "Majors",
    "Technical Skills",
    "Soft Skills",
    "Career Interest",
]

# Check if all features exist
missing_cols = [col for col in features if col not in df.columns]
if missing_cols:
    print(f"❌ ERROR: Missing columns: {missing_cols}")
    print(f"Available columns: {df.columns.tolist()}")
    exit(1)

X = df[features]
y = df["Majors"]

print("="*70)
print("📊 DATA SUMMARY")
print("="*70)
print(f"✓ Features selected: {features}")
print(f"✓ Target variable: 'Majors'")
print(f"✓ Unique career paths: {y.nunique()}")
print(f"✓ Career paths: {y.unique().tolist()}")
print(f"✓ Dataset shape: {X.shape}")
print("="*70 + "\n")

# ---- PREPROCESSING PIPELINE ----
numeric_features = ["Soft Skills Rating"]
categorical_features = ["Majors", "Technical Skills", "Soft Skills", "Career Interest"]

print("🔧 BUILDING PREPROCESSING PIPELINE")
print("-"*70)
print(f"Numeric features:      {numeric_features}")
print(f"Categorical features:  {categorical_features}")
print("-"*70 + "\n")

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
print("="*70)
print("🚀 TRAINING MODEL")
print("="*70)
print("Algorithm: Random Forest Classifier")
print("Estimators: 100")
print("Random state: 42")
print("-"*70)

model.fit(X, y)

print("✓ Model training complete!")
print("="*70 + "\n")

# ---- SAVE MODEL ----
model_path = os.path.join(script_dir, "tryMainmodel.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("="*70)
print("💾 MODEL SAVED SUCCESSFULLY")
print("="*70)
print(f"Model saved at: {model_path}")
print(f"File size: {os.path.getsize(model_path) / 1024:.2f} KB")
print("="*70)

print("\n✅ MODEL TRAINING COMPLETE!")
print("You can now run: python tryMainserver.py\n")