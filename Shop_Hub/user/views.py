from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import MyUser
from .forms import MyUserRegisterForm, MyUserLoginForm
from django.contrib import messages

from .services import generate_otp_code


def user_register_view(request):
    form = MyUserRegisterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Вы успешно создали аккаунт')
        return redirect('index')

    return render(request, 'aut/register.html', context={'form_register':form})

def user_login_view(request):
    form = MyUserLoginForm()
    if request.method == 'POST':
        form = MyUserLoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_password = form.cleaned_data['password']
            user = authenticate(request,username=user_email, password=user_password)
            if user:
                otp_code = generate_otp_code()
                send_mail(
                    subject="Одноразовый код для входа",
                    message=f"{otp_code}",
                    settings.DEFAULT_FROM_EMAIL,
                    fail
                )
                return redirect()
            else:
                messages.error(request, 'error email or password')

    return render(request, 'aut/login.html', context={'form_login':form})

def user_logout_view(request):
    logout(request)
    return redirect('index')

def user_profile_settings_view(request):
    return render(request, 'aut/profile_settings.html')

def otp_verify_view(request, user_id):
    return render(request,)