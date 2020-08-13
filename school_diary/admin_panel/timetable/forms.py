from django import forms
from timetable import models


class LessonCreateForm(forms.ModelForm):
    """Form for creating a new lesson in timetable admin panel."""
    class Meta:
        model = models.Lessons
        fields = ('connection', 'day', 'number', 'subject', 'classroom')
