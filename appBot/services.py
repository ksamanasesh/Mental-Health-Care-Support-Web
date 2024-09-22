import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('api_key')

genai.configure(api_key= api_key)


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
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