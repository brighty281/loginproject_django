from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from .models import register
from django.views.decorators.cache import cache_control
import re
from .decorator import admin_required



@never_cache
@admin_required
def home(request):
    if request.user.is_anonymous :
        print(request.user.is_superuser)
        return redirect('login')
    return render(request,'home.html',{'username': request.user.username})


@never_cache
@admin_required
def Login(request):
    if 'username' in request.session :
        return redirect('/')
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user is not None and not user.is_superuser:
            request.session['username'] = username
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request,"login.html")


@never_cache
@admin_required
def signup(request):
    if 'username' in request.session :
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        try:
            if User.objects.get(username=username):
                messages.error(request, "Username already exists")
                return redirect("signup")
        except:
            pass

        try:
            if User.objects.get(email=email):
                messages.error(request, "Email already exists")
                return redirect("signup")
        except:
            pass

        if not re.match(r'^[\w.@+-]+$',username):
            messages.error(request, "Invalid username")
            return redirect("/signup")

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Invalid email")
            return redirect("/signup")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect("/signup")

        # user = register.objects.create(username=username, email=email, password=password)
        # user.save()

        user2 = User.objects.create_user(username=username, email=email, password=password)
        user2.save()

        messages.success(request, 'Account  created successfully')
        return redirect('login')

    return render(request, 'signup.html')



@never_cache
def Logout(request):
    if request.method=='POST':
        request.session.flush()
        logout(request)
    return redirect('home')
