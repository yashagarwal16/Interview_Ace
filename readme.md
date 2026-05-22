# 🚀 Interview_Ace

An intelligent interview preparation platform that analyzes your resume and generates personalized mock interview questions with AI-powered model answers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)
![Gemini AI](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)

## 🌟 Features

- **📄 Resume Analysis**: Upload PDF/DOC files and automatically extract key information
- **🎯 Role Detection**: AI identifies your role (Backend, Frontend, Data Scientist, etc.) and experience level
- **❓ Smart Questions**: Generates 10 personalized interview questions based on your profile
- **🤖 AI Answers**: Provides model answers using Google's Gemini AI
- **👥 User Management**: Secure registration and login system
- **📊 Multiple Roles Supported**: 
  - Software Engineer (Backend/Frontend)
  - Data Scientist
  - Data Engineer
  - Machine Learning Engineer
  - DevOps Engineer / SRE
  - Cybersecurity Analyst
  - QA Automation Engineer
  - UX/UI Designer
  - Product Manager
  - Data Analyst

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB Atlas
- **AI Service**: Google Gemini API
- **File Processing**: PyMuPDF, python-docx
- **Authentication**: Flask Sessions with password hashing
- **Frontend**: HTML, CSS, JavaScript

## 📋 Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Google Gemini API key

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone  https://github.com/yashagarwal16/Interview_Ace.git
cd interview_Ace
```

### 2. Create Virtual Environment

```bash
python -m venv virtual_env
source virtual_env/bin/activate  # On Windows: virtual_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the `virtual_env` directory:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/interview_prep_ai
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
interview-prep-ai/
├── app.py                 # Main Flask application
├── gemini_api.py         # Google Gemini AI integration
├── granite.py            # Question management and prompting
├── resume_parser.py      # Resume text extraction and analysis
├── interview_ques.json   # Interview questions database
├── requirements.txt      # Python dependencies
├── virtual_env/
│   └── .env             # Environment variables
├── uploads/             # Resume file storage
├── templates/           # HTML templates
│   ├── auth.html
│   └── index.html
└── static/             # CSS, JS, and static files
```

## 🔧 Configuration

### MongoDB Setup

1. Create a MongoDB Atlas account
2. Create a new cluster
3. Get your connection string
4. Add it to your `.env` file

### Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/register` | POST | User registration |
| `/login` | POST | User login |
| `/logout` | GET | User logout |
| `/process-resume` | POST | Upload and process resume |
| `/submit-manual` | POST | Manual role/level submission |
| `/health` | GET | Health check |

## 🎯 Usage

1. **Register/Login**: Create an account or log in
2. **Upload Resume**: Upload your resume in PDF or DOC format
3. **Auto-Detection**: The system automatically detects your role and experience level
4. **Manual Override**: If auto-detection fails, manually select your role and level
5. **Get Questions**: Receive 10 personalized interview questions
6. **Study Answers**: Review AI-generated model answers

## 🔍 Supported File Formats

- **PDF**: `.pdf`
- **Microsoft Word**: `.doc`, `.docx`
- **File Size Limit**: 10MB

## 🤖 AI Features

### Resume Analysis
- Name extraction
- Email detection
- Skills identification
- Role classification
- Experience level assessment

### Question Generation
- Role-specific questions
- Level-appropriate difficulty
- Industry best practices
- Behavioral and technical questions

### Answer Quality
- Concise, professional responses
- Practical examples included
- Appropriate technical depth
- Interview-ready format

## 🛡️ Security Features

- Password hashing with Werkzeug
- Session-based authentication
- File type validation
- Input sanitization
- Error handling and logging

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Test the resume parser:

```bash
python resume_parser.py
```

Test Gemini API connection:

```bash
curl http://localhost:5000/health
```

## 📊 Sample Question Categories

### Junior Level
- Foundational programming concepts
- Basic system design
- Learning agility
- Communication skills

### Mid-Level
- Advanced technical skills
- System architecture
- Project management
- Mentorship capabilities

### Senior/Lead Level
- Strategic thinking
- Technical leadership
- Innovation and emerging tech
- Cross-functional collaboration

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Example with Gunicorn)
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

**"list index out of range"**
- Check if Gemini API key is valid
- Verify MongoDB connection
- Ensure resume contains readable text

**Empty AI responses**
- Check API key permissions
- Verify internet connection
- Review prompt formatting

**Resume parsing fails**
- Ensure file is not corrupted
- Check file format (PDF/DOC/DOCX only)
- Verify file size under 10MB

### Debug Mode

Enable debug mode for detailed error logs:

```python
app.run(debug=True, port=5000)
```

## 📝 Requirements

```txt
Flask==2.3.3
Flask-CORS==4.0.0
pymongo==4.5.0
python-dotenv==1.0.0
PyMuPDF==1.23.5
python-docx==0.8.11
google-generativeai==0.3.0
Werkzeug==2.3.7
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [Yash Agarwal](https://github.com/yashagarwal16)
- LinkedIn: [Yash Agarwal](https://www.linkedin.com/in/yashagarwal-ai?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BXJU03okbRm%2BtDMWNKBoKMw%3D%3D)
- Email: yashagarwala2709@gmail.com

## 🙏 Acknowledgments

- Google Gemini AI for intelligent responses
- MongoDB Atlas for cloud database
- Flask community for the excellent framework
- Contributors and beta testers



⭐ **Star this repository if you found it helpful!**
