import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
from logger import logging  # Assuming you have a custom logger setup
from exception import CustomException

# Load environment variables
load_dotenv()

# Retrieve the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Set up logging configuration

# If GOOGLE_API_KEY is not found, raise an error
if not GEMINI_API_KEY:
    logging.info("GEMINI_API_KEY is missing in the .env file.")
    raise CustomException("GEMINI_API_KEY is missing in the .env file.")
else:
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    logging.info("GEMINI_API_KEY loaded successfully.")

def sanitize_input(text):
    # Remove unwanted characters or trim whitespace if needed
    return text.strip()

def llm_model_object(user_text):
    """Generates a response from Google's Gemini model using the given text."""
    try:
        sanitized_text = sanitize_input(user_text)
        print(f"Sanitized text: {sanitized_text}")  # Debugging step
        genai.configure(api_key= GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(sanitized_text)  # Use sanitized text
        print(f"Response: {response.text}")  # Check if response is valid
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, there was an error processing your request."
