# # chatbot/views.py

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import google.generativeai as genai
# import json

# # Hardcode your API key for testing purposes
# api_key = "AIzaSyAiEj2P1dCH_WL4VZhQCYKIwEkx6wkaay0"
# genai.configure(api_key=api_key)

# # Configure the model
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     generation_config=generation_config,
# )

# # Create a new chat session
# chat_session = model.start_chat(
#     history=[
#         {
#             "role": "user",
#             "parts": ["mental health care chatbot"],
#         },
#         {
#             "role": "model",
#             "parts": ["I am Smith, your mental health care assistant. How can I assist you today?"],
#         },
#     ]
# )

# # Define a view for handling chatbot messages
# @csrf_exempt  # Disable CSRF for this example
# def chat_view(request):
#     if request.method == 'POST':
#         # Parse the user input from the request
#         data = json.loads(request.body)
#         user_message = data.get('message', '')

#         # Send message to the chat session
#         response = chat_session.send_message(user_message)

#         # Return the chatbot response as JSON
#         return JsonResponse({"response": response.text})
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=400)
