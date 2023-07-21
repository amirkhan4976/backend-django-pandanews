from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, UpdateAccountForm
from django.contrib.auth.decorators import login_required
from .models import Account
from django.contrib.auth.hashers import make_password


def login_user_view(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, message="User doesn't exists")

        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            if request.POST.get("next"):
                return redirect(to=request.POST.get("next"))
            return redirect(to="home")
        else:
            messages.error(request, message="Invalid username/password")

    return render(request, template_name="registration/login.html")


@login_required(login_url="login")
def logout_user_view(request):
    logout(request)
    messages.success(request, message="User logged out successfully")
    return redirect(to="login")


def register_user_view(request):
    page = "register"
    ctx = {"page": page}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, message="User registered successfully")
            login(request, user)
            return redirect(to="home")
        else:
            ctx["form"] = form
            return render(request, template_name="registration/login.html", context=ctx)

    return render(request, template_name="registration/login.html", context=ctx)


@login_required(login_url="login")
def user_profile_view(request, pk):
    account = Account.objects.get(id=pk)
    ctx = {"account": account}
    return render(request, template_name="user/user-profile.html", context=ctx)


@login_required(login_url="login")
def update_profile_view(request):
    account = Account.objects.get(id=request.user.account.id)
    if request.method == "POST":
        form = UpdateAccountForm(request.POST, request.FILES, instance=request.user.account)
        if form.is_valid():
            form.save()
            return redirect(to="user-profile", pk=request.user.account.id)

    ctx = {"account": account}
    return render(request, template_name="user/edit-user-profile.html", context=ctx)


@login_required(login_url="login")
def change_password_view(request):
    ctx = {}
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if len(password1) < 5 or len(password2) < 5:
            ctx["Error"] = "Password length should be 5 or more characters"
            return render(request, template_name="user/password-change.html", context=ctx)

        user = User.objects.get(id=request.user.id)
        if not user.check_password(request.POST.get("old_password")):
            ctx["Error"] = "Old password didn't match"
            return render(request, template_name="user/password-change.html", context=ctx)

        if password1 != password2:
            ctx["Error"] = "Confirm password miss-match. Confirm your password"
            return render(request, template_name="user/password-change.html", context=ctx)

        user.password = make_password(password=password1)
        user.save()
        login(request, user)
        return redirect(to="user-profile", pk=request.user.account.id)

    return render(request, template_name="user/password-change.html", context=ctx)
