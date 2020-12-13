from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(
        allow_empty_file=False, widget=forms.FileInput(
            {"class": "custom-file-input"}))
