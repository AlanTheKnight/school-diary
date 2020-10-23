from django.shortcuts import render, redirect, get_object_or_404
from diary.decorators import admin_only
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from news import forms
from news import models


def first_page(request):
    """Redirects user to the first page of news feed."""
    return redirect('news', page=1)


def get_posts(request, page=1):
    """Page where posts are displayed."""
    news = models.Publications.objects.all()
    if "search" in request.GET:  # Posts search
        search_text: str = request.GET.get("search")
        if search_text and not search_text.isspace():
            news = news.filter(title__icontains=search_text)
            search = True
            context = {'news': news, "search": search, "search_text": search_text}
            return render(request, 'news_list.html', context)
    search = False
    news = Paginator(news, 20)
    news = news.get_page(page)
    return render(request, 'news_list.html', {'news': news, "search": search})


def post(request, url):
    """Page where post is showed."""
    article = get_object_or_404(models.Publications, slug=url)
    return render(request, 'news_post.html', {'post': article})


@login_required(login_url="/login/")
@admin_only
def news_create(request):
    """Page where admin can create a new post."""
    form = forms.ArticleCreationForm()
    if request.method == "POST":
        form = forms.ArticleCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_dashboard')
    return render(request, 'news_editor.html', {'form': form})


@login_required(login_url="/login/")
@admin_only
def news_dashboard(request, page):
    """Dashboard for posts."""
    news = models.Publications.objects.all()
    news = Paginator(news, 100)  # 100 posts per page
    news = news.get_page(page)
    return render(request, 'news_dashboard.html', {'news': news})


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
        return redirect('news')
    context = {'item': article}
    return render(request, 'news_delete.html', context)


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
            return redirect('news')
    context = {'form': form, 'data': article}
    return render(request, 'news_editor.html', context)
