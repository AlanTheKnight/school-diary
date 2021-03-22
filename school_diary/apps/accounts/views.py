from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.core.access import unauthenticated_user, allowed_users
from apps.core.users import forms


@unauthenticated_user
def student_registration(request):
    """
    Page with a registration form for students.
    Available only to unauthenticated users.

    Return `registration.html` if form wasn't submitted or isn't valid.
    Otherwise, redirect to `login`.
    """
    form = forms.StudentSignUpForm()
    if request.method == 'POST':
        form = forms.StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'accounts/registration.html', {'form': form})


@unauthenticated_user
def user_login(request):
    """
    Page where user can log in to his account.
    Available only to unauthenticated users.

    Redirect to `homepage` if login was successful.
    Otherwise, return `login.html`.
    """
    form = forms.UsersLogin()
    if request.method == 'POST':
        form = forms.UsersLogin(request.POST)
        if form.is_valid():
            email: str = form.cleaned_data.get('email')
            password: str = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            messages.info(request, 'Проверьте, что вы ввели правильный логин и пароль.')
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    """
    Logout user from a current session and redirect to `login`.
    """
    logout(request)
    return redirect('login')


@login_required(login_url="/login/")
def user_profile(request):
    """
    User profile page. Return 'profile.html`
    """
    return render(request, 'accounts/profile.html')


@allowed_users(allowed_types=(2, 3))
@login_required(login_url="login")
def message_to_admin(request):
    """
    A page where student/teacher can send a message to admin.
    Redirect to 'profile' if message was sent successfully.
    Otherwise, return 'message_to_admin.html'
    """
    form = forms.MessageToAdminForm()
    if request.method == "POST":
        form = forms.MessageToAdminForm(request.POST)
        if form.is_valid():
            form.save(sender=request.user)
            return redirect('profile')
    return render(request, 'accounts/message_to_admin.html', {'form': form})
