# resume_parser.py
import fitz  # PyMuPDF
import re
import os
from docx import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_resume_info(file_path):
    """Extract information from resume file"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get file extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Extract text based on file type
        if file_ext == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif file_ext in ['.doc', '.docx']:
            text = extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        if not text.strip():
            raise ValueError("No text content found in the resume")
        
        # Extract information
        email = extract_email(text)
        name = extract_name(text)
        skills = extract_skills(text)
        role = extract_role(text)
        level = extract_level(text)

        return {
            "email": email,
            "name": name,
            "skills": skills,
            "role": role,
            "level": level
        }
        
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise ValueError("Invalid or corrupted PDF file")

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise ValueError("Invalid or corrupted DOCX file")

def extract_email(text):
    """Extract email address from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else "Not found"

def extract_name(text):
    """Extract name from text"""
    lines = text.strip().split('\n')
    
    # Try to find name in first few lines
    for i, line in enumerate(lines[:5]):
        line = line.strip()
        # Skip empty lines and lines with special characters
        if not line or len(line) < 3:
            continue
            
        # Look for name pattern (2-4 words, starting with capital letters)
        name_pattern = r'^[A-Z][a-z]+(?: [A-Z][a-z]+){1,3}$'
        if re.match(name_pattern, line):
            return line
    
    # Fallback: try to extract from first meaningful line
    for line in lines[:10]:
        line = line.strip()
        if line and len(line.split()) >= 2 and len(line.split()) <= 4:
            words = line.split()
            if all(word[0].isupper() and word[1:].islower() for word in words if len(word) > 1):
                return line
    
    return "Not found"

def extract_skills(text):
    """Extract skills from text"""
    # Comprehensive skills list
    skills_keywords = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask',
        'spring', 'laravel', 'bootstrap', 'jquery', 'sass', 'less', 'webpack', 'gulp',
        
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'cassandra',
        'elasticsearch', 'dynamodb', 'firebase', 'neo4j',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
        'terraform', 'ansible', 'chef', 'puppet', 'vagrant', 'linux', 'unix', 'ubuntu',
        'centos', 'nginx', 'apache', 'git', 'svn', 'ci/cd', 'devops',
        
        # Data Science & ML
        'machine learning', 'deep learning', 'artificial intelligence', 'data science',
        'data analysis', 'statistics', 'pandas', 'numpy', 'scikit-learn', 'tensorflow',
        'pytorch', 'keras', 'opencv', 'nltk', 'spacy', 'matplotlib', 'seaborn', 'plotly',
        'tableau', 'power bi', 'excel', 'jupyter', 'anaconda', 'spark', 'hadoop',
        
        # Mobile Development
        'ios', 'android', 'react native', 'flutter', 'xamarin', 'cordova', 'ionic',
        
        # Testing
        'selenium', 'junit', 'pytest', 'jest', 'mocha', 'cypress', 'postman', 'jmeter',
        'cucumber', 'testng',
        
        # Others
        'agile', 'scrum', 'kanban', 'jira', 'confluence', 'slack', 'teams', 'photoshop',
        'illustrator', 'figma', 'sketch', 'invision', 'zeplin', 'wireframing', 'prototyping',
        'ui/ux', 'user experience', 'user interface', 'graphic design', 'web design',
        'api', 'rest', 'graphql', 'microservices', 'serverless', 'blockchain', 'ethereum',
        'solidity', 'cybersecurity', 'penetration testing', 'vulnerability assessment'
    ]
    
    found_skills = set()
    text_lower = text.lower()
    
    for skill in skills_keywords:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill.title() if len(skill.split()) == 1 else skill)
    
    return list(found_skills) if found_skills else ["Not found"]

def extract_role(text):
    """Extract role/position from text"""
    roles = [
        'data scientist', 'software engineer', 'backend developer', 'frontend developer',
        'full stack developer', 'devops engineer', 'site reliability engineer', 'sre',
        'qa engineer', 'quality assurance', 'test engineer', 'automation engineer',
        'data analyst', 'business analyst', 'product manager', 'project manager',
        'ux designer', 'ui designer', 'graphic designer', 'web designer',
        'machine learning engineer', 'ml engineer', 'data engineer', 'ai engineer',
        'cybersecurity analyst', 'security engineer', 'network administrator',
        'database administrator', 'dba', 'system administrator', 'cloud engineer',
        'solutions architect', 'software architect', 'technical architect',
        'mobile developer', 'ios developer', 'android developer', 'game developer',
        'blockchain developer', 'cryptocurrency developer', 'web3 developer'
    ]
    
    text_lower = text.lower()
    
    # First, try to find exact matches
    for role in roles:
        if role.lower() in text_lower:
            # Map variations to standard roles
            role_mapping = {
                'backend developer': 'Software Engineer (Backend)',
                'frontend developer': 'Software Engineer (Frontend)',
                'full stack developer': 'Software Engineer',
                'devops engineer': 'DevOps Engineer / Site Reliability Engineer (SRE)',
                'site reliability engineer': 'DevOps Engineer / Site Reliability Engineer (SRE)',
                'sre': 'DevOps Engineer / Site Reliability Engineer (SRE)',
                'qa engineer': 'QA Automation Engineer',
                'quality assurance': 'QA Automation Engineer',
                'test engineer': 'QA Automation Engineer',
                'automation engineer': 'QA Automation Engineer',
                'ux designer': 'UX/UI Designer',
                'ui designer': 'UX/UI Designer',
                'graphic designer': 'UX/UI Designer',
                'web designer': 'UX/UI Designer',
                'ml engineer': 'Machine Learning Engineer',
                'ai engineer': 'Machine Learning Engineer',
                'security engineer': 'Cybersecurity Analyst',
                'mobile developer': 'Software Engineer (Frontend)',
                'ios developer': 'Software Engineer (Frontend)',
                'android developer': 'Software Engineer (Frontend)',
                'blockchain developer': 'Software Engineer (Backend)'
            }
            
            return role_mapping.get(role.lower(), role.title())
    
    return "Not found"

def extract_level(text):
    """Extract experience level from text"""
    text_lower = text.lower()
    
    # Keywords for different levels
    senior_keywords = [
        'senior', 'lead', 'principal', 'architect', 'manager', 'director',
        'head of', 'chief', 'vp', 'vice president', '5+ years', '6+ years',
        '7+ years', '8+ years', '9+ years', '10+ years'
    ]
    
    junior_keywords = [
        'junior', 'entry', 'graduate', 'intern', 'trainee', 'associate',
        'fresh', 'new grad', '0-2 years', '1 year', '2 years'
    ]
    
    mid_keywords = [
        'mid', 'intermediate', '3 years', '4 years', '5 years',
        '3-5 years', '2-4 years'
    ]
    
    # Check for senior level
    for keyword in senior_keywords:
        if keyword in text_lower:
            return 'Senior/Lead/Architect'
    
    # Check for junior level
    for keyword in junior_keywords:
        if keyword in text_lower:
            return 'Junior'
    
    # Check for mid level
    for keyword in mid_keywords:
        if keyword in text_lower:
            return 'Mid-Level'
    
    # Try to extract years of experience using regex
    years_pattern = r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)'
    matches = re.findall(years_pattern, text_lower)
    
    if matches:
        years = int(matches[0])
        if years <= 2:
            return 'Junior'
        elif years <= 5:
            return 'Mid-Level'
        else:
            return 'Senior/Lead/Architect'
    
    return "Not found"

def validate_resume_content(text):
    """Validate if the text contains resume-like content"""
    if not text or len(text.strip()) < 100:
        return False, "Resume content is too short"
    
    # Check for common resume indicators
    resume_indicators = [
        'experience', 'education', 'skills', 'work', 'employment',
        'qualification', 'degree', 'university', 'college', 'project',
        'responsibility', 'achievement', 'objective', 'summary'
    ]
    
    text_lower = text.lower()
    found_indicators = sum(1 for indicator in resume_indicators if indicator in text_lower)
    
    if found_indicators < 2:
        return False, "Content does not appear to be a resume"
    
    return True, "Valid resume content"

# Additional utility functions for file validation
def is_valid_resume_file(file_path, max_size_mb=10):
    """Validate resume file before processing"""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > max_size_mb * 1024 * 1024:
            return False, f"File size exceeds {max_size_mb}MB limit"
        
        # Check file extension
        allowed_extensions = ['.pdf', '.doc', '.docx']
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in allowed_extensions:
            return False, f"Unsupported file type: {file_ext}"
        
        # Try to extract and validate content
        if file_ext == '.pdf':
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_docx(file_path)
        
        is_valid, message = validate_resume_content(text)
        if not is_valid:
            return False, message
        
        return True, "Valid resume file"
        
    except Exception as e:
        return False, f"Error validating file: {str(e)}"

# Test function
def test_resume_parser():
    """Test function for resume parser"""
    # This is for testing purposes
    sample_text = """
    John Smith
    john.smith@email.com
    
    Software Engineer with 3 years of experience
    
    Skills: Python, JavaScript, React, Node.js, SQL, AWS
    
    Experience:
    - Software Developer at Tech Company (2021-2024)
    - Worked on web applications using modern technologies
    
    Education:
    - Bachelor's in Computer Science
    """
    
    result = {
        "email": extract_email(sample_text),
        "name": extract_name(sample_text),
        "skills": extract_skills(sample_text),
        "role": extract_role(sample_text),
        "level": extract_level(sample_text)
    }
    
    print("Test Results:")
    for key, value in result.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_resume_parser()