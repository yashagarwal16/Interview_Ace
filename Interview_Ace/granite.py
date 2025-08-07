# granite.py

import json
import random

# ✅ Get questions for a specific role and level
def get_questions_by_role_and_level(role, level, filepath="interview_ques.json", max_questions=10):
    """Get questions for a role and level, limiting to max_questions"""
    with open(filepath, "r") as f:
        data = json.load(f)

    framework = data.get("qualitativeInterviewFramework", [])
    all_questions = []

    for entry in framework:
        if entry["role"].lower() == role.lower():
            for lvl in entry["levels"]:
                if lvl["level"].lower() == level.lower():
                    for comp in lvl["competencyAreas"]:
                        all_questions.extend(comp["qualitativeQuestionExamples"])

    # If we have more questions than needed, randomly select max_questions
    if len(all_questions) > max_questions:
        all_questions = random.sample(all_questions, max_questions)
    
    return all_questions

# ✅ Get all available roles
def get_all_roles(filepath="interview_ques.json"):
    with open(filepath, "r") as f:
        data = json.load(f)
    return [item["role"] for item in data.get("qualitativeInterviewFramework", [])]

# ✅ Get all levels for a given role
def get_levels_for_role(role, filepath="interview_ques.json"):
    with open(filepath, "r") as f:
        data = json.load(f)
    for item in data.get("qualitativeInterviewFramework", []):
        if item["role"].lower() == role.lower():
            return [lvl["level"] for lvl in item["levels"]]
    return []

# ✅ Format a prompt to send to Gemini with better structure
def format_prompt_for_granite(role, level, questions):
    """Create a well-structured prompt for Gemini API"""
    prompt = f"""You are an expert interview coach preparing model answers for a {level} {role} candidate.

IMPORTANT INSTRUCTIONS:
- Provide concise, professional answers (2-3 sentences each)
- Answer each question with practical examples and specific details
- Use a {level.lower()} level of technical depth
- Format your response EXACTLY as shown below
- Number each answer clearly

Please provide model answers for the following {len(questions)} interview questions:

"""
    
    # Add numbered questions
    for i, question in enumerate(questions, 1):
        prompt += f"{i}. {question}\n"
    
    prompt += f"""

RESPONSE FORMAT:
Answer each question in this exact format:

1. [Your concise answer for question 1 - 2-3 sentences with specific examples]

2. [Your concise answer for question 2 - 2-3 sentences with specific examples]

3. [Your concise answer for question 3 - 2-3 sentences with specific examples]

...and so on for all {len(questions)} questions.

Remember: Keep answers professional, practical, and appropriate for a {level} {role} candidate."""
    
    return prompt