from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if password != confirm_password:
            messages.error(request, "Password does not match!")
            return redirect("account:register")

        if len(password) < 6:
            messages.error(request, "Password must be atleast 6 characters or more!")
            return redirect("account:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "User already exists with this email!")
            return redirect("account:register")

        new_user = User.objects.create_user(
            username=email, email=email, password=password
        )
        new_user.save()
        messages.info(request, "User created successfully please login")
        return redirect("account:login")

    return render(request, "account/register.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)
                next_page = request.GET.get("next", "index")
                messages.success(request, "Login successful")
                return redirect(next_page)
            else:
                messages.error(request, "Invalid credentials")
                return redirect("account:login")
        else:
            messages.error(request, "User does not exist")
            return redirect("account:login")
    return render(request, "account/login.html")


def logout_view(request):
    messages.success(request, "You are logged out successfully")
    logout(request)
    return redirect("index")
