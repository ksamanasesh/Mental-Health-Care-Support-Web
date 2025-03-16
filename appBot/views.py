from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
import json
import logging
from .models import UserDetails, ChatMessage  # Updated model names
from .forms import userForm
from .services import chat_session, get_special_response  # Import chat configuration

# Test Route
def testing(request):
    return HttpResponse('<h1>Mental Health Care Support</h1>')

# SignUp View
def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(pass1) < 8:
            return render(request, 'signUp.html', {'min_words': "Password must contain at least 8 characters"})

        if pass1 != pass2:
            return render(request, 'signUp.html', {'noMatch': "Passwords don't match"})

        user = User.objects.create_user(username=username, email=email, password=pass1, first_name=fname, last_name=lname)
        user.save()

        login(request, user)  # Auto-login after signup
        return redirect('home')

    return render(request, 'signUp.html')

# SignIn View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            # Store user info in session
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            request.session.set_expiry(0)  # Expire session when browser closes

            return redirect('home')
        else:
            return render(request, 'signIn.html', {'error': "Incorrect Username or Password"})

    return render(request, 'signIn.html')

# Home View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='signIn')
def home(request):
    return render(request, 'home.html', {'welcome': f"Hello, {request.user.first_name}"})

# Logout View
@login_required(login_url='signIn')
def signOut(request):
    logout(request)
    request.session.flush()
    return redirect('signIn')

# User Profile Creation
@login_required(login_url='signIn')
def user_profile(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile_view')
    else:
        form = userForm()
    return render(request, 'user_profile.html', {'form': form})

# View User Profile
@login_required(login_url='signIn')
def user_profile_view(request):
    user_detail = UserDetails.objects.all()
    return render(request, "user_profile_view.html", {'user_details': user_detail})

# Chat View with Persistent Chat History
logger = logging.getLogger(__name__)

@login_required(login_url='signIn')
@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            # Check authentication
            if not request.user.is_authenticated:
                logger.warning("User session expired or authentication failed.")
                return JsonResponse({"error": "Session expired. Please log in again."}, status=401)

            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({"error": "Message cannot be empty"}, status=400)

            logger.info(f"User {request.user.username} sent: {user_message}")

            # Check for predefined responses (Dr. Smith's identity and developer info)
            special_response = get_special_response(user_message)
            if special_response:
                return JsonResponse({"response": special_response})

            # Retrieve last 10 messages to maintain context
            chat_history = list(ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:10].values_list('user_message', 'bot_response'))
            chat_history.reverse()  # Order from oldest to newest

            # Format history for chat session
            formatted_history = []
            for user_msg, bot_resp in chat_history:
                formatted_history.append({"role": "user", "parts": [user_msg]})
                formatted_history.append({"role": "model", "parts": [bot_resp]})

            # Update chat session history
            chat_session.history = formatted_history

            # Get AI response
            response = chat_session.send_message(user_message)
            bot_response = response.text if response else "I'm here to listen. How can I support you today?"

            # Save chat to DB
            ChatMessage.objects.create(user=request.user, user_message=user_message, bot_response=bot_response)

            logger.info(f"Bot response: {bot_response}")

            return JsonResponse({"response": bot_response})

        except Exception as e:
            logger.error(f"Chat error: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Something went wrong"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# Retrieve Chat History
@login_required(login_url='signIn')
def get_chat_history(request):
    user = request.user
    chat_history = ChatMessage.objects.filter(user=user).order_by("timestamp")

    messages = [
        {"role": "user", "message": chat.user_message, "timestamp": chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        for chat in chat_history
    ] + [
        {"role": "model", "message": chat.bot_response, "timestamp": chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        for chat in chat_history
    ]

    return JsonResponse({"chat_history": messages})

# Chat Page
@login_required(login_url='signIn')
def chat_page(request):
    return render(request, 'chat.html', {'csrf_token': get_token(request)})
