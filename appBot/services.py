import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Load API key from environment variables
# api_key = os.getenv('api_key')

genai.configure(api_key='AIzaSyAiEj2P1dCH_WL4VZhQCYKIwEkx6wkaay0')

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 75,
    "response_mime_type": "text/plain",
}

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start chat session with predefined history
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["mental health care chatbot"],
        },
        {
            "role": "model",
            "parts": ["I am Smith, your mental health care assistant. How can I assist you today?"],
        },
    ]
)

# Function to check for predefined responses based on user message
def get_special_response(user_message):
    user_message = user_message.lower()

    # Consistent response about the bot
    bot_identity_response = (
        "I am Smith, your virtual psychiatrist, developed by Team Citronix. "
        "I am here to assist you with mental health care and emotional well-being."
    )

    if "who are you" in user_message or "what is your name" in user_message:
        return bot_identity_response
    
    if "who developed you" in user_message:
        return bot_identity_response

    return None
