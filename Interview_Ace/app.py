# app.py
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime
from resume_parser import extract_resume_info
from granite import (
    get_questions_by_role_and_level,
    get_levels_for_role,
    get_all_roles,
    format_prompt_for_granite
)
from gemini_api import get_gemini_response

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key
CORS(app)

# MongoDB connection
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Explicit path to .env inside virtual_env
load_dotenv(dotenv_path=os.path.join("virtual_env", ".env"))

try:
    MONGODB_URI = os.getenv("MONGODB_URI")
    client = MongoClient(MONGODB_URI)
    db = client['interview_prep_ai']
    users_collection = db['users']
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print(f"❌ MongoDB Atlas connection failed: {e}")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed file extensions for resume
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_resume_file(file):
    """Validate uploaded resume file"""
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, "Invalid file type. Please upload PDF, DOC, or DOCX files only."
    
    # Check file size (approximate, since we're reading in memory)
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    
    if size > MAX_FILE_SIZE:
        return False, "File size too large. Maximum size allowed is 10MB."
    
    return True, "Valid file"

def parse_gemini_response(response_text, questions):
    """Parse Gemini response and match with questions - improved version"""
    import re
    import logging
    
    logger = logging.getLogger(__name__)
    
    if not response_text or not response_text.strip():
        logger.warning("Empty response from Gemini")
        return [{"question": q, "answer": "No response generated."} for q in questions]
    
    logger.info(f"Parsing response of length {len(response_text)} for {len(questions)} questions")
    
    # Clean the response
    response_text = response_text.strip()
    
    # Method 1: Try to parse numbered responses
    parsed_questions = []
    
    # Split by numbered patterns (1., 2., 3., etc.)
    pattern = r'\n?(\d+)\.\s*'
    parts = re.split(pattern, response_text)
    
    if len(parts) > 2:  # We have numbered sections
        logger.info(f"Found {(len(parts)-1)//2} numbered sections")
        
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                question_num = int(parts[i]) - 1  # Convert to 0-based index
                answer_text = parts[i + 1].strip()
                
                # Clean up the answer
                answer_text = re.sub(r'\*\*.*?\*\*', '', answer_text)  # Remove markdown bold
                answer_text = re.sub(r'AI Model Answer', '', answer_text)
                answer_text = re.sub(r'---+', '', answer_text)
                answer_text = re.sub(r'\n+', ' ', answer_text)  # Replace multiple newlines with space
                answer_text = answer_text.strip()
                
                if question_num < len(questions) and answer_text:
                    parsed_questions.append({
                        "question": questions[question_num],
                        "answer": answer_text
                    })
    
    # Method 2: If Method 1 didn't work well, try alternative parsing
    if len(parsed_questions) < len(questions) * 0.8:  # If we got less than 80% of questions
        logger.warning("Method 1 failed, trying alternative parsing")
        parsed_questions = []
        
        # Try splitting by double newlines or other patterns
        sections = re.split(r'\n\s*\n+', response_text)
        sections = [s.strip() for s in sections if s.strip()]
        
        for i, question in enumerate(questions):
            if i < len(sections):
                answer = sections[i]
                # Clean the answer
                answer = re.sub(r'^\d+\.\s*', '', answer)  # Remove leading number
                answer = re.sub(r'\*\*.*?\*\*', '', answer)  # Remove markdown
                answer = re.sub(r'AI Model Answer', '', answer)
                answer = answer.strip()
                
                if not answer:
                    answer = "Answer not available."
            else:
                answer = "Answer not available."
            
            parsed_questions.append({
                "question": question,
                "answer": answer
            })
    
    # Method 3: Fallback - ensure we have answers for all questions
    if len(parsed_questions) != len(questions):
        logger.warning(f"Mismatch: {len(parsed_questions)} parsed vs {len(questions)} expected")
        
        # Fill missing questions
        for i in range(len(parsed_questions), len(questions)):
            parsed_questions.append({
                "question": questions[i],
                "answer": "Answer not available due to parsing error."
            })
        
        # Trim excess if any
        parsed_questions = parsed_questions[:len(questions)]
    
    logger.info(f"Successfully parsed {len(parsed_questions)} question-answer pairs")
    return parsed_questions

@app.route("/")
def index():
    if 'user_id' not in session:
        return render_template("auth.html")
    return render_template("index.html", user=session.get('user_name'))

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not all([name, email, password]):
            return jsonify({"success": False, "message": "All fields are required"}), 400
        
        if len(password) < 6:
            return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400
        
        # Check if user already exists
        if users_collection.find_one({"email": email}):
            return jsonify({"success": False, "message": "Email already registered"}), 400
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        }
        
        result = users_collection.insert_one(user_data)
        
        # Set session
        session['user_id'] = str(result.inserted_id)
        session['user_name'] = name
        session['user_email'] = email
        
        return jsonify({"success": True, "message": "Registration successful!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Registration failed: {str(e)}"}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not all([email, password]):
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        # Find user
        user = users_collection.find_one({"email": email})
        if not user or not check_password_hash(user['password'], password):
            return jsonify({"success": False, "message": "Invalid email or password"}), 400
        
        # Set session
        session['user_id'] = str(user['_id'])
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        
        return jsonify({"success": True, "message": "Login successful!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Login failed: {str(e)}"}), 500

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/process-resume", methods=["POST"])
def process_resume():
    if 'user_id' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        uploaded_file = request.files["resume"]
        
        # Validate file
        is_valid, message = validate_resume_file(uploaded_file)
        if not is_valid:
            return jsonify({"error": message, "invalid_file": True}), 400

        # Save the uploaded file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"{session['user_id']}_{uploaded_file.filename}")
        uploaded_file.save(filepath)

        # Extract resume information
        info = extract_resume_info(filepath)
        
        role = info.get("role")
        level = info.get("level")
        all_roles = get_all_roles()

        # Check if we need manual input
        needs_manual = False
        if not role or role not in all_roles:
            needs_manual = True
        else:
            levels = get_levels_for_role(role)
            if not level or level not in levels:
                needs_manual = True

        if needs_manual:
            return jsonify({
                "needsManualInput": True,
                "info": info,
                "availableRoles": all_roles
            })

        # Process automatically
        questions = get_questions_by_role_and_level(role, level)
        if not questions:
            return jsonify({"error": f"No questions found for {role} ({level})"}), 400

        prompt = format_prompt_for_granite(role, level, questions)

        response = get_gemini_response(prompt)
        parsed_questions = parse_gemini_response(response, questions)

        return jsonify({
            "needsManualInput": False,
            "info": info,
            "questions": parsed_questions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/submit-manual", methods=["POST"])
def submit_manual():
    if 'user_id' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    try:
        data = request.get_json()
        
        role = data.get("role")
        level = data.get("level")
        name = data.get("name")
        email = data.get("email")
        skills = data.get("skills", "").split(", ") if data.get("skills") else []

        # Validate inputs
        if not all([role, level, name]):
            return jsonify({"error": "Missing required fields"}), 400

        levels = get_levels_for_role(role)
        if level not in levels:
            return jsonify({"error": f"Level '{level}' not valid for role '{role}'"}), 400

        info = {
            "name": name,
            "email": email,
            "skills": [skill.strip() for skill in skills if skill.strip()],
            "role": role,
            "level": level
        }

        questions = get_questions_by_role_and_level(role, level)
        if not questions:
            return jsonify({"error": f"No questions found for {role} ({level})"}), 400

        prompt = format_prompt_for_granite(role, level, questions)
        response = get_gemini_response(prompt)
        parsed_questions = parse_gemini_response(response, questions)

        return jsonify({
            "info": info,
            "questions": parsed_questions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)