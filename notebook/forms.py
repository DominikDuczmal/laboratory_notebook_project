from django import forms
from .models import Analyst, Task


class AnalystForm(forms.ModelForm):
    """Analyst ModelForm mapping closely to Django model Analyst.

    It is used to create a form that lets Users submit their personal data.
    """

    class Meta:
        model = Analyst
        fields = ['first_name', 'last_name', 'email', 'laboratory']


class TaskForm(forms.ModelForm):
    """Task ModelForm mapping closely to Django model Task.

    It is used to create a form that lets Users submit/change their Tasks.
    """

    class Meta:
        model = Task
        fields = ['subject', 'content', 'photos']
