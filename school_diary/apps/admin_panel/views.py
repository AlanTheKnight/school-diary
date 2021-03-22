from django.shortcuts import render
from apps.core.access import admin_only
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
@admin_only
def main(request):
    return render(request, 'admin_panel.html')
