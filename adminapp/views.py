from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib import messages
import re
from django.views.decorators.cache import never_cache


@never_cache
def admin_home(request):
    if request.user.is_anonymous and not request.user.is_superuser:
        return redirect('admin_login')
    return render(request,'admin_home.html',{'username':request.session.get('super_user')})


@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_home')
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=uname, password=password)

        if user is not None and user.is_superuser and user.is_active:
            request.session['super_user']=uname
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, "Invalid credentials. Please Try again.")
            return redirect('admin_login')
    return render(request, 'admin_login.html')

@never_cache
def user_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        result = User.objects.all().exclude(username='admin')
        return render(request, 'user_list.html',{'users':result})
    else:
        messages.info(request, "Please log in as admin")
        return render(request,'admin_login.html')


@never_cache
def edit_user(request, uid):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=uid)
        if request.method == 'POST':
            new_username = request.POST['username']
            new_email = request.POST['email']

            try:
                existing_user_with_username = User.objects.get(username=new_username)
                if existing_user_with_username != user:
                    messages.error(request, "Username already exists")
                    return redirect('edit_user', uid=uid)
            except User.DoesNotExist:
                pass

            try:
                existing_user_with_email = User.objects.get(email=new_email)
                if existing_user_with_email != user:
                    messages.error(request, "Email already exists")
                    return redirect('edit_user', uid=uid)
            except User.DoesNotExist:
                pass

            user.username = new_username
            user.email = new_email

            try:
                user.save()
            except Exception as e:
                print(f"Error while saving user: {e}")

            return redirect('user_list')
                                        
        return render(request, "edit_user.html", {'user': user})

    else:
        messages.info(request, "Please log in as admin")
        return render(request, 'admin_login.html')



@never_cache
def delete_user(request,uid):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=uid)
        user.delete()
        return redirect('user_list')
    else:
        messages.info(request, "Please log in as admin")
        return render(request,'admin_login.html')



@never_cache
def search_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        query = request.GET.get('search')
        if query:
            results = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
        else:
            results = User.objects.all()
        return render(request, 'search_result.html', {'results': results})
    else:
        messages.info(request, "Please log in as admin")
        return render(request, 'admin_login.html')


@never_cache
def add_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method=='POST':
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('pass1')
            try:
                if User.objects.get(username=username):
                    messages.error(request, "Username already exists")
                    return redirect("add_user")
            except:
                pass

            try:
                if User.objects.get(email=email):
                    messages.error(request, "Email already exists")
                    return redirect("add_user")
            except:
                pass

            if not re.match(r'^[\w.@+-]+$', username):
                messages.error(request, "Invalid username")
                return redirect("/admin_adduser")

            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                messages.error(request, "Invalid email")
                return redirect("add_user")

            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters")
                return redirect("add_user")

            user=User.objects.create_user(username,email,password)
            user.save()
            if user is not None:
                messages.success(request, "User added successfully")
                return redirect('user_list')
            else:
                return render(request,'add_user.html')
        return render(request,'add_user.html')

    else:
        messages.info(request, "Please log in as admin")
        return render(request,'admin_login.html')


@never_cache
def admin_logout(request):
    if request.user.is_authenticated and request.user.is_superuser:
        request.session.flush()
        logout(request)
        return redirect('admin_login')
    else:
        messages.info(request, "Please log in as admin")
        return render(request,'admin_login.html')

