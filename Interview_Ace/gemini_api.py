# gemini_api.py
import google.generativeai as genai
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Use environment variable for API key (more secure)
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDvPt0numvbuoj1l1HLgurcjoojqhv9Wmc")
genai.configure(api_key=API_KEY)

def get_gemini_response(prompt):
    """Get response from Gemini API with better configuration"""
    try:
        if not prompt or not prompt.strip():
            raise ValueError("Empty prompt provided")
        
        logger.info(f"Sending prompt to Gemini API (length: {len(prompt)})")
        
        # Configure the model with specific parameters for better responses
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  # Updated model name
            generation_config={
                "temperature": 0.3,  # Lower temperature for more consistent responses
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 4000,  # Increased for longer responses
            }
        )
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            logger.error("Empty response from Gemini API")
            raise ValueError("Empty response from Gemini API")
        
        logger.info(f"Received response from Gemini API (length: {len(response.text)})")
        
        # Log first 200 characters for debugging (without sensitive data)
        logger.debug(f"Response preview: {response.text[:200]}...")
        
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise Exception(f"Gemini API failed: {e}")

def test_gemini_connection():
    """Test function to verify Gemini API is working"""
    try:
        test_prompt = "Say 'Hello, API is working!' in exactly that format."
        response = get_gemini_response(test_prompt)
        return True, response
    except Exception as e:
        return False, str(e)