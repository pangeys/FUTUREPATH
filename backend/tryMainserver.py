from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'simple_key'  # Add this line to enable sessions
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
    for root, dirs, files in os.walk(STATIC_DIR):
        level = root.replace(STATIC_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}✓ {file}")
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

# --- Data Base Connection Setup ---

# ---- DATABASE CONFIGURATION (Added for MySQL connection) ----
import mysql.connector
from mysql.connector import Error

# Database configuration (matches XAMPP defaults; update if you changed credentials)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Empty for default; set if you added a password
    'database': 'userID'  # Your database name from XAMPP
}
    
# Function to get a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
@app.route('/test_db')
def test_db():
    connection = get_db_connection()
    if connection:
        connection.close()
        return "Connected to MySQL successfully!"
    else:
        return "Failed to connect to MySQL. Check XAMPP and db_config."

# ---- ROUTES ----

# Home page (Nicole's landing page)
@app.route("/")
def home():
    return render_template("Nicole(Home).html")

# Signup page
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not fullname or not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('signup'))
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (fullname, username, email, password) VALUES (%s, %s, %s, %s)",
                    (fullname, username, email, password)
                )
                connection.commit()
                flash('Signup successful! Please log in.', 'success')
                return redirect(url_for('home'))
            except mysql.connector.IntegrityError:
                flash('Username or email already exists.', 'error')
            except Error as e:
                flash(f'Database error: {e}', 'error')
            finally:
                cursor.close()
                connection.close()
        else:
            flash('Database connection failed.', 'error')
    
    return render_template("signup.html")

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('home'))
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, fullname, username, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if user and user['password'] == password:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['fullname'] = user['fullname']
                flash('Login successful!', 'success')
                return redirect(url_for('predictor'))  # Redirect to your predictor page
            else:
                flash('Invalid username or password.', 'error')
        else:
            flash('Database connection failed.', 'error')
    
    return render_template('Nicole(Home).html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))

# Course page
@app.route("/course")
def course():
    return render_template("Airon(Course).html")

# About page (redirects to home with anchor)
@app.route("/about")
def about():
    return render_template("Darrel(AboutUs).html")

# Contact page
@app.route("/contact")
def contact():
    return render_template("Marco(ContactUs).html")

# Career predictor page
@app.route("/predictor")
def predictor():
    return render_template("tryMain.html")

# ---- PREDICTION API ----
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print(f"\n🎯 Prediction request received")
        print(f"Data: {data}")
        
        # Check for the correct column names that match the model
        required = [
            "Major",
            "Technical Skills",
            "Soft Skills",
            "Soft Skills Rating",
            "Career Interest",
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