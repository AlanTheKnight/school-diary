from django import forms
from apps.core import models


class StudentSearchForm(forms.Form):
    """
    Form that helps head teachers search
    students before adding them to class.
    """
    email = forms.CharField(
        label="Почта", required=False, max_length=100)
    first_name = forms.CharField(
        label="Имя", required=False, max_length=100)
    surname = forms.CharField(
        label="Фамилия", required=False, max_length=100)

    def get_students(self):
        email = self.data.get('email')
        fn = self.data.get('first_name')
        s = self.data.get('surname')
        if fn or s or email:
            return models.Students.objects.select_related("account").filter(
                account__first_name__icontains=fn, account__surname__icontains=s,
                account__email__icontains=email)
        return []


class KlassCreationForm(forms.ModelForm):
    """Form for creating a new class."""
    class Meta:
        model = models.Klasses
        fields = ('number', 'letter', 'subjects', 'teachers')


class KlassSettingsForm(forms.ModelForm):
    class Meta:
        model = models.Klasses
        fields = ('subjects', 'teachers')
