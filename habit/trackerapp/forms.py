from django import forms
from .models import Habit, CheckIn

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'category', 'frequency', 'start_date']

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn 
        fields = ['date', 'note']
