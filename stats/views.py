from django.shortcuts import render, redirect
from django.utils.timezone import datetime
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Avg
import pandas as pd
import plotly.express as px
from plotly.offline import plot
from .forms import RegisterForm, LogInForm, RoundForm, HoleForm, HoleFormSet, HoleFront9FormSet, HoleBack9FormSet, RoundToggleForm
from .models import RoundModel, HoleModel


# Create your views here.

@login_required(login_url='/registration/login')
def index(request):
        round_type = request.GET.get('round_type', 'all')
        tee_type = request.GET.get('tee_type', 'all')

        form = RoundToggleForm(initial={'round_type': round_type})
        round = RoundModel.objects.filter(user=request.user)

        if round_type == '18':
                round = round.filter(is_18_holes=True)
        elif round_type == '9':
                round = round.filter(is_18_holes=False)
        
        if tee_type != 'all':
                round = round.filter(tees=tee_type)

        if round.exists():
                data = {
                        'Fairways': [r.fairways for r in round],
                        'GIR': [r.greens for r in round],
                        'Round': [r.date for r in round],
                        'Putts': [r.putts for r in round],
                        'Score': [r.score for r in round],
                }

                df = pd.DataFrame(data)

                fig = px.scatter(df,
                        x=[r.date for r in round],
                        y=['Score'],
                        title='Scores',
                        labels={'x': 'Date', 'y': 'Score'}
                )

                chart = fig.to_html()

                fig2 = px.box(
                        df.melt(id_vars=['Round'], value_vars=['Fairways', 'GIR', 'Putts']),
                        x='variable',
                        y='value', 
                        title='Distribution of Fairways, GIR and Putts per Round',
                        labels={'variable': 'Fairways & Greens', 'value': 'Value'}
                )

                box_chart = fig2.to_html()

                scoring_avg = round.aggregate(Avg('score', default=0))['score__avg']
                total_rounds = round.count()

                context = {'chart': chart, 'form': form, 'round_type': round_type, 'tee_type': tee_type, 'box_chart': box_chart, 'scoring_avg': scoring_avg, 'total_rounds': total_rounds,}


        else:
                context = {'message': 'Enter some scores to retrieve your data', 'form': form, 'round_type': round_type}

        return render(request, 'stats/index.html', context)


def login_user(request):
        if request.method == "POST":
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                        auth.login(request, user)
                        messages.success(request, (f"Sup, {username}. You have been successfully logged in!"))
                        return redirect('index') 
                
                else:
                        messages.error(request, 'Unable to login, wrong username or password.')
                        return redirect('index')

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


def about(request):
        return render(request, 'stats/about.html')


@login_required(login_url='/registration/login')
def round_entry(request):
        if request.method == 'POST':
                round_form = RoundForm(request.POST)
                hole_formset = HoleFormSet(request.POST, queryset=HoleModel.objects.none())

                if round_form.is_valid() and hole_formset.is_valid():
                        round = round_form.save(commit=False)
                        round.user = request.user
                        round.is_18_holes = True
                        round.is_front_9 = False
                        total_score = 0
                        total_fairways = 0
                        total_greens = 0
                        total_putts = 0
                        round.save()

                        for form in hole_formset:
                                hole = form.save(commit=False)
                                hole.round = round
                                total_score += hole.score
                                total_fairways += hole.fairway
                                total_greens += hole.gir
                                total_putts += hole.putts
                                hole.save()
                        
                        round.score = total_score
                        round.fairways = total_fairways
                        round.greens = total_greens
                        round.putts = total_putts
                        round.save()
                        
                        return redirect('index')

        else:
                round_form = RoundForm()
                hole_formset = HoleFormSet(queryset=HoleModel.objects.none())

                for i, form in enumerate(hole_formset.forms):
                        form.initial['hole_number'] = i + 1

        return render(request, 'stats/round_entry.html', {'round_form': round_form, 'hole_formset': hole_formset,})


@login_required(login_url='/registration/login')
def front_9(request):
        if request.method == "POST":
                round_form = RoundForm(request.POST)
                hole_formset = HoleFormSet(request.POST, queryset=HoleModel.objects.none())

                if round_form.is_valid() and hole_formset.is_valid():
                        round = round_form.save(commit=False)
                        round.user = request.user
                        round.is_18_holes = False
                        round.is_front_9 = True
                        total_score = 0
                        total_fairways = 0
                        total_greens = 0
                        total_putts = 0
                        round.save()
                        
                        for form in hole_formset:
                                hole = form.save(commit=False)
                                hole.round = round
                                total_score += hole.score
                                total_fairways += hole.fairway
                                total_greens += hole.gir
                                total_putts += hole.putts
                                hole.save()
                        
                        round.score = total_score
                        round.fairways = total_fairways
                        round.greens = total_greens
                        round.putts = total_putts
                        round.save()
                        
                        return redirect('index')
                
                else:
                        print(round_form.errors)
                        print(hole_formset.errors)

        else:
                round_form = RoundForm()
                hole_formset = HoleFront9FormSet(queryset=HoleModel.objects.none())

                for i, form in enumerate(hole_formset.forms):
                        form.initial['hole_number'] = i + 1

        return render(request, 'stats/front_9_entry.html', {'round_form': round_form, 'hole_formset': hole_formset,})


@login_required(login_url='/registration/login')
def back_9(request):
        if request.method == "POST":
                round_form = RoundForm(request.POST)
                hole_formset = HoleFormSet(request.POST, queryset=HoleModel.objects.none())

                if round_form.is_valid() and hole_formset.is_valid():
                        round = round_form.save(commit=False)
                        round.user = request.user
                        round.is_18_holes = False
                        round.is_front_9 = False
                        total_score = 0
                        total_fairways = 0
                        total_greens = 0
                        total_putts = 0
                        round.save()
                
                        for form in hole_formset:
                                hole = form.save(commit=False)
                                hole.round = round
                                total_score += hole.score
                                total_fairways += hole.fairway
                                total_greens += hole.gir
                                total_putts += hole.putts
                                hole.save()
                        
                        round.score = total_score
                        round.fairways = total_fairways
                        round.greens = total_greens
                        round.putts = total_putts
                        round.save()
                        
                        return redirect('index')
        
        else:
                round_form = RoundForm
                hole_formset = HoleBack9FormSet(queryset=HoleModel.objects.none())

                for i, form in enumerate(hole_formset.forms, start= 9):
                        form.initial['hole_number'] = i + 1

        return render(request, 'stats/back_9_entry.html', {'round_form': round_form, 'hole_formset': hole_formset,})