from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import MyUser,OPT
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta

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
            user = authenticate(request, username=user_email, password=user_password)
            if user:
                otp_code = generate_otp_code()

                request.session['otp_code'] = otp_code
                request.session['otp_user_id'] = user.id

                OPT.objects.create(user=user, code=otp_code)

                send_mail(
                    subject="ErjanHolding",
                    message=f'''
                        Одноразовый код для входа
                                {otp_code}        
                        ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email]
                )

                return redirect('2FA')
            else:
                messages.error(request, 'Неверный email или пароль.')
    return render(request, 'aut/login.html', context={'form_login': form})


def user_logout_view(request):
    logout(request)
    return redirect('index')


def user_profile_settings_view(request):
    return render(request, 'aut/profile_settings.html')


def otp_verify_view(request):
    user_id = request.session.get('otp_user_id')

    if not user_id:
        messages.error(request, 'Сессия истекла. Пожалуйста, войдите снова.')
        return redirect('login')

    if request.method == 'POST':
        input_code = request.POST.get('otp_code')

        otp_record = OPT.objects.filter(user_id=user_id).order_by('-created_at').first()

        if otp_record:
            if otp_record.created_at > now() - timedelta(minutes=5) and otp_record.code == input_code:
                user = otp_record.user
                login(request, user)
                del request.session['otp_code']
                del request.session['otp_user_id']
                return redirect('index')
            else:
                messages.error(request, 'Код недействителен или истёк')
        else:
            messages.error(request, 'Код не найден')

    return render(request, 'aut/2FA.html')

