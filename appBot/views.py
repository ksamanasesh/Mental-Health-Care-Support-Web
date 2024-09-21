from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import user_details,ChatMesage
from .forms import user_details
from fuzzywuzzy import fuzz
from .services import get_bot_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

# Create your views here.

def testing(request):
    text = '<h1>Mental Health Care Support</h1>'
    return HttpResponse(text)

def signUp(request):
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    numeric = False
    similarity = 55
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        similar = fuzz.ratio(username,pass1)

        if len(pass1) < 8 :
            min_words = "Password must contain atleast 8 characters"
            return render(request,'signUp.html',context={'min_words':min_words})

        else:
            for letter in pass1:
                if letter in numbers:
                    numeric = True
            
            if numeric is not True:
                numeric_char = "Password must contain atleast one numeric charater"
                return render(request,'signUp.html',context={'numeric_char':numeric_char})
            else:
                if similar >= similarity:
                    same_words = "Password and Username is too similar"
                    return render(request,'signUp.html',context={'same_words':same_words})
                else:
                    if pass1 == pass2 :
                        createUser = User.objects.create_user(first_name=fname,last_name=lname,username=username, email=email, password=pass1)
                        createUser.first_name = fname
                        createUser.last_name = lname
                        createUser.save()
                    else :
                        noMatch = "Password doesn't match"
                        return render(request,'signUp.html',context={'noMatch':noMatch})
            
                    success = "Your account has been created Successfully, Login Here"
                    return redirect('/signIn')
    return render(request,'signUp.html')

def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username, password=password)
        if user is not None :
            lname = user.last_name
            welcome = f"Hello, {lname}"
            login(request, user)
            return render(request,'home.html',context={'welcome':welcome})
        else :
            error = "Incorrect Username or Password"
            return render(request,'signIn.html',context={'error':error})
    return render(request,'signIn.html')

def home(request):
    return render(request,'home.html')

def signOut(request):
    logout(request)
    logOut = "Successfully logged Out"
    return render(request,'home.html',context={'logOut':logOut})

def user_profile(request):
    if request.method == 'POST':
        form = user_details(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user_profile_view')
        else:
            form = user_details
            return render(request,'user_profile.html',{'form':form})
    return render(request,'user_profile.html')

def user_profile_view(request):
    user_detail = user_details.object.all()
    user_info = {'user_details': user_detail}
    return render(request,"user_profile_view.html", user_info)

# chatbot/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json

# Hardcode your API key for testing purposes
api_key = "AIzaSyAiEj2P1dCH_WL4VZhQCYKIwEkx6wkaay0"
genai.configure(api_key=api_key)

# Configure the model
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

# Create a new chat session
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

# Define a view for handling chatbot messages
@csrf_exempt  # Disable CSRF for this example
def chat_view(request):
    if request.method == 'POST':
        # Parse the user input from the request
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Send message to the chat session
        response = chat_session.send_message(user_message)

        # Return the chatbot response as JSON
        return JsonResponse({"response": response.text})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
