from django import forms
from .models import Habit, HabitLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'goal_type', 'goal_value', 'frequency']

class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ['completed_at', 'value']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']