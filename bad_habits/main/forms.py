from django import forms
from .models import Habit, HabitLog

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'goal_type', 'goal_value', 'frequency']

class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ['completed_at', 'value']