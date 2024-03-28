from django.shortcuts import render, HttpResponse
from app.forms import *
from django.core.mail import send_mail
# Create your views here.

def register(request):
    UFO = UserForm()
    PFO = ProfileForm()
    d = {'UFO':UFO, 'PFO':PFO}
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST, request.FILES)
        if UFDO.is_valid():
            MUFDO = UFDO.save(commit=False)
            pw = UFDO.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO = PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            message=f'Hello {UFDO.cleaned_data["username"]} you r registration is successfull'
            send_mail(
                'Registration Successfull',
                message,
                'likith.qsp@gmail.com',
                [UFDO.cleaned_data['email']],
                fail_silently=False,
            )
            return render(request, 'login.html')
        return HttpResponse('Invalid Details')

    return render(request,'register.html', d)


def user_login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')