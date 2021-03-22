from django.shortcuts import render, redirect

from . import forms


def main(request):
    groupCreationForm = forms.NotesGroupCreationForm()
    if request.method == "POST" and "addNoteGroup" in request.POST:
        groupCreationForm = forms.NotesGroupCreationForm(request.POST)
        if groupCreationForm.is_valid():
            noteGroup = groupCreationForm.save(commit=False)
            noteGroup.author = request.user
            noteGroup.save()
            return redirect("notes:notes")

    return render(request, 'notes/notes/notes.html', {
        "form": groupCreationForm
    })
