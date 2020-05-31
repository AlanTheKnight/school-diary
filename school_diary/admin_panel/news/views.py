from django.shortcuts import render, redirect
from diary.decorators import admin_only
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from admin_panel.news import forms
from news import models


@login_required(login_url="/login/")
@admin_only
def news_create(request):
    """Page where admin can create a new post."""
    if request.method == "POST":
        form = forms.ArticleCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_dashboard')
    form = forms.ArticleCreationForm()
    return render(request, 'news/news_editor.html', {'form': form})


@login_required(login_url="/login/")
@admin_only
def news_dashboard(request, page):
    """Dashboard for posts."""
    news = models.Publications.objects.all()
    news = Paginator(news, 100)  # 100 posts per page
    news = news.get_page(page)
    return render(request, 'news/news_dashboard.html', {'news': news})


@login_required(login_url="/login/")
@admin_only
def news_dashboard_first_page(request):
    """Redirects user to the first page of the dashboard."""
    return redirect('news_dashboard', page=1)


@login_required(login_url="/login/")
@admin_only
def news_delete(request, pk):
    """Page where admin deletes a post."""
    article = models.Publications.objects.get(id=pk)
    if request.method == "POST":
        article.delete()
        return redirect('/news/dashboard')
    context = {'item': article}
    return render(request, 'news/news_delete.html', context)


@login_required(login_url="/login/")
@admin_only
def news_update(request, pk):
    """Page where post can be edited."""
    article = models.Publications.objects.get(id=pk)
    form = forms.ArticleCreationForm(instance=article)
    if request.method == 'POST':
        form = forms.ArticleCreationForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            if request.POST.get('deleteimage') is not None:
                article.image = ''
                article.save()
            return redirect('news_dashboard')
    context = {'form': form, 'data': article}
    return render(request, 'news/news_editor.html', context)
