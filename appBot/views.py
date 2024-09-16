from django.shortcuts import render,HttpResponse

# Create your views here.

def testing(request):
    text = '<h1>Mental Health Care Support</h1>'
    return HttpResponse(text)