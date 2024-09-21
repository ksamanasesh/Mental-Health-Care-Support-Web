import google.generativeai as genai


api_key = "AIzaSyAiEj2P1dCH_WL4VZhQCYKIwEkx6wkaay0"


genai.configure(api_key=api_key)


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
            "parts": [
                "mental health care chatbot",
            ],
        },
        {
            "role": "model",
            "parts": [
                "I can't provide medical advice, and a chatbot can't replace a qualified mental health professional. However, I can help you create a basic chatbot that might offer some helpful resources and information. Here's a framework for a basic mental health care chatbot:\n\n"
                "1. Greeting and Initial Questions:\n"
                "* Chatbot: 'Hello! I'm here to help you find resources and information about mental health. How can I assist you today?'\n"
                "* User: 'I'm feeling stressed.'\n"
                "* Chatbot: 'I understand. Can you tell me more about what you're feeling stressed about?'\n"
                "...\n"
                "Always prioritize safety and ethical considerations when developing a chatbot for mental health support."
            ],
        },
        {
            "role": "user",
            "parts": [
                "and the bot name is Smith\n",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Okay, here's a sample interaction with Smith, the mental health chatbot, incorporating the features we discussed: \n\n"
                "**User:** Hey, I'm feeling really stressed lately.\n\n"
                "**Smith:** Hi there! I understand that stress can be tough. Can you tell me more about what's causing you stress?\n"
                "...",
            ],
        },
    ]
)

print("You can type 'exit' to quit the chat.")
while True:

    user_input = input("You: ")

    
    if user_input.lower() in ["exit", "quit"]:
        print("Smith: Goodbye! Take care of yourself.")
        break

     
    response = chat_session.send_message(user_input)

    
    print("Smith:", response.text)
