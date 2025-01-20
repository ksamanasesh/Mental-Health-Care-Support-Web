import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('api_key')

genai.configure(api_key=api_key)


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 75,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


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

    if "who are you" in user_message:
        return "I am Smith, your virtual psychiatrist created to assist with mental health care and stress relief."
    
    if "who developed you" in user_message:
        return "I was developed by team Citronix, a virtual psychiatrist, designed to help with mental health care and emotional well-being."

    if "what is your name" in user_message:
        return "I am Smith, your virtual psychiatrist. How can I assist you today?"

    return None
