from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from .forms import User, UserLoginForm, ContactForm

# Create your views here.
def register(request):

    if request.method == "POST":
        form = User(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно")
            return redirect("index")
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = User()
    return render(request, "user/register.html", {"form": form})


def user_login(request):
    if request.POST:
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = UserLoginForm()
    return render(request, "user/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("user_login")


def sendMail(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data["subject"],
                form.cleaned_data["content"],
                request.user.email,
                ["admin@gmail.com"],
            )
            if mail:
                messages.success(request, "Письмо отправлено успешно")
                return redirect("sendMail")
            else:
                messages.error(request, "Ошибка отправки письма")
        else:
            messages.error(request, "Ошибка отправки письма")
    else:
        form = ContactForm()
    return render(request, "user/send.html", {"form": form})
