from core import models
from django.shortcuts import render
import openpyxl
from . import forms
from io import BytesIO


# def processData(data):
#     try:
#         book: openpyxl.Workbook = openpyxl.load_workbook(
#             filename=BytesIO(data.read()))
#     except Exception:
#         return "Файл не может быть загружен. Проверьте, что вы отправили правильный Excel-документ."
#     sheets = book.get_sheet_names()
#     for sheet_name in sheets:
#         sheet: openpyxl.worksheet.worksheet.Worksheet = book.get_sheet_by_name(sheet_name)
        

def main(request):
    result = None
    form = forms.FileUploadForm()
    if request.method == "POST":
        form = forms.FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data["file"]
            # result = processData(data)
    return render(request, "upload/main.html", {'form': form, "result": result})
