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
from .models import UserDetails, ChatMessage
from .forms import userForm
from .services import chat_session, get_special_response
from collections import Counter
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Configure logging
logger = logging.getLogger(__name__)

# Download required NLTK resources
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# BASIC ROUTES
def testing(request):
    return HttpResponse('<h1>Mental Health Care Support</h1>')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def design(request):
    return render(request, 'design.html')

def contact(request):
    return render(request, 'contact.html')


# AUTHENTICATION ROUTES
def signUp(request):
    """Handles user registration"""
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(pass1) < 8:
            return render(request, 'signUp.html', {'min_words': "Password must be at least 8 characters"})

        if pass1 != pass2:
            return render(request, 'signUp.html', {'noMatch': "Passwords don't match"})

        user = User.objects.create_user(username=username, email=email, password=pass1, first_name=fname, last_name=lname)
        user.save()
        login(request, user)
        return redirect('home')

    return render(request, 'signUp.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signIn(request):
    """Handles user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            request.session.set_expiry(0)
            return redirect('home')
        else:
            return render(request, 'signIn.html', {'error': "Incorrect Username or Password"})

    return render(request, 'signIn.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        welcome_message = f"Hello, {request.user.first_name}"
    else:
        welcome_message = "Hello, Guest"

    return render(request, 'home.html', {'welcome': welcome_message})

@login_required(login_url='signIn')
def signOut(request):
    """Handles user logout"""
    logout(request)
    request.session.flush()
    return redirect('signIn')

# USER PROFILE MANAGEMENT
@login_required(login_url='signIn')
def user_profile(request):
    """Handles user profile creation"""
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile_view')
    else:
        form = userForm()
    return render(request, 'user_profile.html', {'form': form})

@login_required(login_url='signIn')
def user_profile_view(request):
    """Displays user profile details"""
    user_detail = UserDetails.objects.all()
    return render(request, "user_profile_view.html", {'user_details': user_detail})


# CHAT FUNCTIONALITY
@login_required(login_url='signIn')
@csrf_exempt
def chat_view(request):
    """Handles user chatbot interaction"""
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Session expired. Please log in again."}, status=401)

            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({"error": "Message cannot be empty"}, status=400)

            special_response = get_special_response(user_message)
            if special_response:
                return JsonResponse({"response": special_response})

            # Retrieve last 10 messages to maintain context
            chat_history = list(ChatMessage.objects.filter(user=request.user)
                                 .order_by('-timestamp')[:10]
                                 .values_list('user_message', 'bot_response'))
            chat_history.reverse()  # Order from oldest to newest

            # Format history for chat session
            formatted_history = [
                {"role": "user", "parts": [user_msg]}
                if index % 2 == 0 else {"role": "model", "parts": [bot_resp]}
                for index, (user_msg, bot_resp) in enumerate(chat_history)
            ]

            # Assign history to chat session
            chat_session.history = formatted_history

            # Get AI response
            response = chat_session.send_message(user_message)
            bot_response = response.text if response else "I'm here to listen. How can I support you today?"

            # Format bot response for proper HTML rendering
            bot_response = bot_response.replace('* **', '<br>').replace('**', '=>')  # Convert Markdown to HTML

            # Save chat to database
            ChatMessage.objects.create(user=request.user, user_message=user_message, bot_response=bot_response)

            return JsonResponse({"response": bot_response})

        except Exception as e:
            logger.error(f"Chat error: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Something went wrong"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required(login_url='signIn')
def get_chat_history(request):
    """Retrieves user's chat history"""
    user_chats = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
    messages = [{"role": "user", "message": chat.user_message, "timestamp": chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for chat in user_chats]
    messages += [{"role": "model", "message": chat.bot_response, "timestamp": chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for chat in user_chats]

    return JsonResponse({"chat_history": messages})

@login_required(login_url='signIn')
def chat_page(request):
    """Renders chatbot UI"""
    return render(request, 'chat.html', {'csrf_token': get_token(request)})


# CHAT DATA ANALYSIS

@login_required
def get_chat_data(request):
    """Generates chatbot analytics"""
    user_chats = ChatMessage.objects.filter(user=request.user).order_by('timestamp')

    sentiments = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    for chat in user_chats:
        sentiment_score = sia.polarity_scores(chat.user_message)['compound']
        if sentiment_score >= 0.05:
            sentiments['Positive'] += 1
        elif sentiment_score <= -0.05:
            sentiments['Negative'] += 1
        else:
            sentiments['Neutral'] += 1

    sentiment_counts = [sentiments['Positive'], sentiments['Neutral'], sentiments['Negative']]
    daily_chats = Counter(chat.timestamp.date() for chat in user_chats)
    chat_dates, chat_counts = zip(*sorted(daily_chats.items())) if daily_chats else ([], [])

    return JsonResponse({
        "sentiment_counts": sentiment_counts,
        "chat_dates": list(chat_dates),
        "chat_counts": list(chat_counts),
    })

@login_required
def chatbot_dashboard(request):
    """Renders chatbot analytics dashboard"""
    return render(request, 'dashboard.html')
