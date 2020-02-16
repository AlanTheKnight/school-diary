from django import forms
from .models import Documents

class GetMinimumForm(forms.Form):
    subject = forms.ChoiceField(label="Предмет:", choices=[
        ("Информатика", "Информатика"),
        ("История", "История"),
        ("Литература", "Литература"),
        ("Математика", "Математика"),
        ("Обществознание", "Обществознание"),
        ("Русский язык", "Русский язык"),
        ("Химия и биология", "Хим-Био"),
        ("Экономика", "Экономика"),
        ("Физика", "Физика")])
    grade = forms.ChoiceField(label="Класс:", choices=[
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11)])
    term = forms.ChoiceField(label="Четверть:", choices=[
        (1, "I"),
        (2, "II"),
        (3, "III"),
        (4, "IV")])


class MinimumCreationForm(forms.ModelForm):
    class Meta:
        fields = ('subject', 'grade', 'term', 'file')
        model = Documents
        widgets = {
            'subject':forms.Select(attrs={'class':'form-control'}),
            'grade':forms.Select(attrs={'class':'form-control'}),
            'term':forms.Select(attrs={'class':'form-control'}),
            'file':forms.FileInput(attrs={'class':'form-control-file'}),
        }