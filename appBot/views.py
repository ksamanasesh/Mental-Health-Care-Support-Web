from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from fuzzywuzzy import fuzz

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

def user_profile(requet):
    if request.method == 'POST':
        