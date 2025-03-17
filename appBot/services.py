import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Load API key securely
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Store in .env file for security

# Generation configuration
generation_config = {
    "temperature": 0.7,  # Balanced randomness for a natural tone
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 512,  # Increased to avoid response cut-off
    "response_mime_type": "text/plain",
}

# Initialize the Gemini model for Dr. Smith, the friendly mental health chatbot
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start chat session with a warm greeting
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["You are Dr. Smith, a friendly and supportive mental health chatbot. "
                      "Your goal is to provide comfort, empathy, and guidance to users who may be struggling."],
        },
        {
            "role": "model",
            "parts": ["Hello! I'm Dr. Smith, your friendly mental health assistant. 💙\n\n"
                      "How are you feeling today? I'm here to listen and support you."],
        },
    ]
)

# Function to format AI response with proper line breaks
def format_response(response_text):
    """Formats AI response to ensure bullet points and sections start on a new line."""
    # Ensure each "**" or "* **" starts on a new line
    formatted_text = response_text.replace("* **", "\n\n**").replace("\n*", "\n\n*")
    
    # Fix spacing issues & strip leading/trailing whitespace
    formatted_text = formatted_text.strip()
    
    return formatted_text

# Function to check for predefined responses based on user message
def get_special_response(user_message):
    """Returns predefined responses for identity-related or developer questions."""
    user_message = user_message.lower()

    identity_response = (
        "I'm Dr. Smith, your virtual mental health assistant. 😊\n\n"
        "I'm here to offer guidance, support, and a listening ear."
    )

    developer_response = (
        "I was developed by **Team Citronix**, a passionate group dedicated to AI-powered mental health care.\n\n"
        "My purpose is to provide compassionate and supportive guidance."
    )

    if "who are you" in user_message or "what is your name" in user_message:
        return identity_response
    
    if "who developed you" in user_message or "who created you" in user_message:
        return developer_response

    return None  # If no special response, allow AI to generate a response

# Function to process user input dynamically with friendly responses
def chat_with_bot(user_message):
    """Handles user input and generates a response from Dr. Smith."""
    user_message = user_message.strip()

    # Check for predefined responses
    special_response = get_special_response(user_message)
    if special_response:
        return special_response

    # Get AI-generated response
    response = chat_session.send_message(user_message)

    # Check for truncation (if response is incomplete)
    if response and response.text and response.text.endswith(("I", "and", "to", "but", "because", "so", "the", "that")):
        response = chat_session.send_message("Can you continue?")

    # Format response to move '**' points to a new paragraph
    return format_response(response.text) if response else "I'm here for you. How can I support you today? 💙"
