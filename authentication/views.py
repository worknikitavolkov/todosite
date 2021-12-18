from django.shortcuts import redirect, render
from django.contrib import messages
from validate_email import validate_email
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import User
from helpers.decorators import auth_user_no_access

@auth_user_no_access
def register_user(req):
    if req.method == "POST":
        context = {"has_error": False, "data": req.POST}
        email = req.POST.get("email")
        username = req.POST.get("username")
        password = req.POST.get("password")
        password2 = req.POST.get("password2")

        if not validate_email(email):
            messages.add_message(req, messages.ERROR,
                                 "Enter a valid email address")
            context["has_error"] = True
        elif not username:
            messages.add_message(req, messages.ERROR,
                                 "Username is required")
            context["has_error"] = True
        elif User.objects.filter(username=username).exists():
            messages.add_message(req, messages.ERROR,
                                 "Username is taken!")
            context["has_error"] = True
        elif User.objects.filter(email=email).exists():
            messages.add_message(req, messages.ERROR,
                                 "Email is taken!")
            context["has_error"] = True
        elif len(password) < 6:
            messages.add_message(req, messages.ERROR,
                                 "Password should be at least 6 characters")
            context["has_error"] = True
        elif password != password2:
            messages.add_message(req, messages.ERROR,
                                 "Password mismatch")
            context["has_error"] = True

        if context["has_error"]:
            return render(req, "authentication/register.html", context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.add_message(req, messages.SUCCESS,
                             "Account created, you can now login!")
        return redirect("login")

    return render(req, "authentication/register.html")

@auth_user_no_access
def login_user(req):
    if req.method == "POST":
        context = {"data": req.POST}
        username = req.POST.get("username")
        password = req.POST.get("password")

        user = authenticate(req, username=username, password=password)

        if not user:
            messages.add_message(req, messages.ERROR,
                                 "Invalid credentials")
            return render(req, "authentication/login.html", context)

        login(req, user)
        messages.add_message(req, messages.SUCCESS,
                             f"Welcome, {user.username}!")

        return redirect(reverse("home"))

    return render(req, "authentication/login.html")


def logout_user(req):
    logout(req)
    messages.add_message(req, messages.SUCCESS,
                         "Successfully logged out")
    return redirect(reverse("login"))
