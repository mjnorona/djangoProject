import bcrypt
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def index(request):

    list = User.objects.all()
    # for i in list:
    #     print i.email
    return render(request, 'project/index.html')


def register(request):

    if request.method == "POST":
        values = User.objects.register(request.POST)
        if values[0]:
            request.session['id'] = values[1]
            return redirect("/success")
        else:
            for error in values[1]:
                messages.error(request, error)
            return redirect("/")



def login(request):
    if request.method == "POST":
        login = User.objects.login(request.POST)
        # print login
        if login[0]:

            request.session['id'] = login[2]
            return redirect('/success')
        else:
            messages.error(request, 'Email or password is incorrect')
            return redirect('/')

def success(request):
    return render(request, 'project/success.html')

def logout(request):
    request.session.clear()
    return redirect('/')
