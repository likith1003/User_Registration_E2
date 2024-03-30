from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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


def home(request):
    if request.session.get('username'):
        un = request.session['username']
        d = {'un':un}
        return render(request, 'home.html', d)
    return render(request, 'home.html')



def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO and AUO.is_active:
            login(request, AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse('Invalid Credentials')
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'home.html')

@login_required
def user_profile(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    PO = Profile.objects.get(username=UO)
    d = {'UO':UO, 'PO':PO}
    return render(request, 'user_profile.html', d)


@login_required
def change_password(request):
    un = request.session.get('username')
    if request.method == 'POST':
        pw = request.POST.get('password')
        UO = User.objects.get(username=un)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password changed Successfully')
    return render(request, 'change_password.html')