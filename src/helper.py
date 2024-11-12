import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
from logger import logging  # Assuming you have a custom logger setup
from exception import CustomException  # Assuming you have a custom exception class

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

def voice_input():
    """Captures audio from the microphone and converts it to text."""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        logging.info("Listening...")
        audio = r.listen(source)

    try:
        # Using Google Web Speech API to recognize the speech
        text = r.recognize_google(audio)
        logging.info(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        logging.info("Sorry, could not understand the audio.")
        return None
    except sr.RequestError as e:
        logging.info(f"Could not request result from Google Speech Recognition service: {e}")
        return None

def text_to_speech(text):
    """Converts text to speech and saves it as an MP3 file."""
    if text:
        try:
            tts = gTTS(text=text, lang="en")
            tts.save("speech.mp3")
            logging.info("Speech saved as speech.mp3")
        except Exception as e:
            logging.info(f"Error converting text to speech: {e}")
    else:
        logging.warning("No text provided for speech conversion.")

def llm_model_object(user_text):
    """Generates a response from Google's Gemini model using the given text."""
    try:
        # Configure Google API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Create a Generative Model instance (Gemini model)
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate content based on user input
        response = model.generate_content(user_text)
        
        # Extract and return the generated content
        result = response.text
        logging.info(f"Model response: {result}")
        return result
    except Exception as e:
        logging.info(f"Error generating content from the model: {e}")
        return f"Sorry, there was an error processing your request: {str(e)}"

