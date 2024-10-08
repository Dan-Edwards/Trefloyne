from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import RoundModel, HoleModel, TEES_CHOICES

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            'username': None,
            'password1': 'Minimum 8 characters'
        }

class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class RoundForm(forms.ModelForm):
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )

    class Meta:
        model = RoundModel
        fields = ['date', 'course_name', 'tees']

class HoleForm(forms.ModelForm):
    class Meta:
        model = HoleModel
        fields = ['hole_number', 'hole_par', 'score', 'fairway', 'gir', 'putts']
        widgets = {
            'hole_number': forms.HiddenInput(),
        }


HoleFormSet = modelformset_factory(HoleModel, form=HoleForm, extra=18)

HoleFront9FormSet = modelformset_factory(HoleModel, form=HoleForm, extra=9)

HoleBack9FormSet = modelformset_factory(HoleModel, form=HoleForm, extra=9)

class RoundToggleForm(forms.Form):
    ROUND_CHOICES = (
        ('all', 'All Rounds'),
        ('18', '18 Holes'),
        ('9', '9 Holes'),
    )

    round_type = forms.ChoiceField(choices=ROUND_CHOICES, required=False, label="Round Type")
    tee_type = forms.ChoiceField(choices=TEES_CHOICES, required=False, label="Tees")