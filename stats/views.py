from django.shortcuts import render, redirect
from django.utils.timezone import datetime
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import authenticate, logout, login
from django.core.mail import send_mail
from .forms import RegisterForm, LogInForm, RoundForm, HoleForm, HoleFormSet
from .models import RoundModel, HoleModel


# Create your views here.

def index(request):
        return render(request, 'stats/index.html')

def login_user(request):
        
        if request.method == "POST":
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                        auth.login(request, user)
                        messages.success(request, ("You have been successfully logged in!"))
                        return redirect('index') 
                
                else:
                        messages.error(request, 'Unable to login, wrong username or password.')
                        return redirect('stats/registration/login.html')

        else:
                form = LogInForm()
        
        return render(request, 'stats/registration/login.html', {"form":form})


def logout_user(request):
        logout(request)
        messages.success(request, ("You have been successfully logged out!"))
        return redirect('stats/registration/logout.html')


def user_register(request):
        if request.method == "POST":
                form = RegisterForm(request.POST)
                if form.is_valid():
                        form.save()
                        username = form.cleaned_data.get('username')
                        messages.success(request, f'Account created successfully for {username}!')
                        subject = "Trefloyne Stats"
                        message = f"Nice one {username}! Your account is ready to start entering how many 3 stabs you've had."
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [request.POST['email']])
        
                        return redirect("/")

        else:
                form = RegisterForm()
        
        return render(request, 'stats/registration/register.html', {"form":form})


def name(request, name):
        print(request.build_absolute_uri()) #optional
        return render(
                request,
                'stats/name.html',
                {
                    'name': name,
                    'date': datetime.now()
                }
            )


def about(request):
        return render(request, 'stats/about.html')


def round_entry(request):
        if request.method == 'POST':
                round_form = RoundForm(request.POST)
                hole_formset = HoleFormSet(request.POST, queryset=HoleModel.objects.none())

                if round_form.is_valid() and hole_formset.is_valid():
                        round = round_form.save()

                        for form in hole_formset:
                                hole = form.save(commit=False)
                                hole.round = round
                                hole.save()
                        
                        return redirect('index')

        else:
                round_form = RoundForm()
                hole_formset = HoleFormSet(queryset=HoleModel.objects.none())

                for i, form in enumerate(hole_formset.forms):
                        form.initial['hole_number'] = i + 1

        return render(request, 'stats/round_entry.html', {'round_form': round_form, 'hole_formset': hole_formset,})


def front_9(request):
        return render(request, 'stats/front_9_entry.html')


def back_9(request):
        return render(request, 'stats/back_9_entry.html')