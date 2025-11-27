from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# ---- SIMPLE PATH SETUP ----
# Get absolute path to this file's directory (backend folder)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")

# Tell Flask where to find templates and static files
app.template_folder = TEMPLATES_DIR
app.static_folder = STATIC_DIR

print("\n" + "="*70)
print("📁 CHECKING FILE STRUCTURE")
print("="*70)
print(f"Backend folder:   {BACKEND_DIR}")
print(f"Frontend folder:  {FRONTEND_DIR}")
print(f"Static folder:    {STATIC_DIR}")
print(f"Templates folder: {TEMPLATES_DIR}")
print("-"*70)

# Check if folders exist
print("Folder Status:")
print(f"  Frontend exists:  {os.path.exists(FRONTEND_DIR)}")
print(f"  Static exists:    {os.path.exists(STATIC_DIR)}")
print(f"  Templates exists: {os.path.exists(TEMPLATES_DIR)}")

# List files in static folder
if os.path.exists(STATIC_DIR):
    print("\n📄 Files in static folder:")
    files = os.listdir(STATIC_DIR)
    if files:
        for f in files:
            print(f"  ✓ {f}")
    else:
        print("  ❌ NO FILES FOUND!")
else:
    print("\n❌ STATIC FOLDER DOESN'T EXIST!")
    print(f"   Expected location: {STATIC_DIR}")

print("="*70 + "\n")

# ---- LOAD MODEL ----
MODEL_PATH = os.path.join(BACKEND_DIR, "tryMainmodel.pkl")
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✓ Model loaded successfully!\n")
except FileNotFoundError:
    print(f"❌ ERROR: Model not found at {MODEL_PATH}")
    print("Run 'python tryMainmodel.py' first!\n")
    exit(1)

# ---- HOME PAGE ----
@app.route("/")
def home():
    # ✅ USE render_template() - this processes {{ url_for() }} syntax
    return render_template("tryMain.html")

# ---- PREDICTION API ----
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print(f"\n🎯 Prediction request received")
        print(f"Data: {data}")
        
        # ✅ UPDATED: Check for the correct column names that match your model
        required = [
            "Rating.1",           # Programming Languages Ratings
            "Rating",             # Soft Skills Ratings
            "Current Course",
            "Technical Skills",
            "Projects",
            "Challenges"
        ]
        
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"success": False, "error": f"Missing: {missing}"}), 400
        
        # Make prediction
        df = pd.DataFrame([data])
        prediction = model.predict(df)
        
        print(f"✓ Prediction: {prediction[0]}\n")
        
        return jsonify({
            "success": True,
            "prediction": prediction[0]
        })
    
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return jsonify({"success": False, "error": str(e)}), 500

# ---- RUN SERVER ----
if __name__ == "__main__":
    print("="*70)
    print("🚀 STARTING FLASK SERVER")
    print("="*70)
    print("🌐 Open in browser: http://127.0.0.1:5000")
    print("⌨️  Press CTRL+C to stop")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5000)