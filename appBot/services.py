import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Load API key securely
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Store in .env file for security

# Generation configuration
generation_config = {
    "temperature": 0.7,  # Balanced randomness
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 200,  # Allow longer responses for deeper conversations
    "response_mime_type": "text/plain",
}

# Initialize the Gemini model for Dr. Smith, the mental health care chatbot
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start chat session with a meaningful conversation history
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["You are Dr. Smith, a mental health care chatbot. Respond with empathy and guidance."],
        },
        {
            "role": "model",
            "parts": ["Hello, I am Dr. Smith, your virtual mental health assistant. How are you feeling today?"],
        },
    ]
)

# Function to check for predefined responses based on user message
def get_special_response(user_message):
    """Returns predefined responses for specific identity-related questions."""
    user_message = user_message.lower()

    # Consistent identity response
    identity_response = (
        "I am Dr. Smith, your virtual psychiatrist and mental health assistant. "
        "I am here to listen, support, and guide you toward emotional well-being."
    )

    # Consistent developer response
    developer_response = (
        "I was developed by **Team Citronix**, a group dedicated to advancing AI-powered mental health care. "
        "My purpose is to provide compassionate support and helpful guidance."
    )

    if "who are you" in user_message or "what is your name" in user_message:
        return identity_response
    
    if "who developed you" in user_message or "who created you" in user_message:
        return developer_response

    return None  # If no special response, return None to allow AI to generate a response

# Function to process user input dynamically
def chat_with_bot(user_message):
    """Handles user input and generates a response from Dr. Smith."""
    user_message = user_message.strip()

    # Check for predefined responses
    special_response = get_special_response(user_message)
    if special_response:
        return special_response

    # Ask Gemini for a response
    response = chat_session.send_message(user_message)

    return response.text if response else "I'm here to listen. How can I support you today?"
