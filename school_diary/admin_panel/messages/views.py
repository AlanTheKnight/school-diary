from django.shortcuts import render, redirect
from diary.decorators import admin_only
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import diary.models as models


@login_required(login_url="/login/")
@admin_only
def messages_dashboard_first_page(request):
    """Redirect a user to the first page of the dashboard."""
    return redirect('messages_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def messages_dashboard(request, page):
    u = models.AdminMessages.objects.all()
    u = Paginator(u, 100)
    u = u.get_page(page)
    return render(request, 'messages/dashboard.html', {'users': u})


@login_required(login_url="/login/")
@admin_only
def messages_delete(request, pk):
    s = models.AdminMessages.objects.get(id=pk)
    if request.method == "POST":
        s.delete()
        return redirect('messages_dashboard')
    return render(request, 'messages/delete.html', {'s': s})


@login_required(login_url="/login/")
@admin_only
def messages_view(request, pk):
    s = models.AdminMessages.objects.get(id=pk)
    return render(request, 'messages/view.html', {'s': s})