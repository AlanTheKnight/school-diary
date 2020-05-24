from django import forms
import diary.models as models


bts4attr = {'class': 'form-control'}


class AddStudentToGradeForm(forms.Form):
    email = forms.CharField(
        label="Почта", required=False, max_length=100, widget=forms.TextInput(attrs=bts4attr))
    first_name = forms.CharField(
        label="Имя", required=False, max_length=100, widget=forms.TextInput(attrs=bts4attr))
    surname = forms.CharField(
        label="Фамилия", required=False, max_length=100, widget=forms.TextInput(attrs=bts4attr))


class GradeCreationForm(forms.ModelForm):
    class Meta:
        model = models.Grades
        fields = ('number', 'letter', 'subjects', 'teachers')
        widgets = {
            'number': forms.Select(attrs=bts4attr),
            'letter': forms.Select(attrs=bts4attr),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'subjects'}),
            'teachers': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'teachers'}),
        }


class ClassSettingsForm(forms.ModelForm):
    class Meta:
        model = models.Grades
        fields = ('subjects', 'teachers')
        widgets = {
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'subjects'}),
            'teachers': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'teachers'}),
        }
