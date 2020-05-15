from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Publications
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .forms import ArticleCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_only
from django.contrib import messages


def first_page(request):
    """
    Redirects user to the first page with posts.
    """
    return redirect('/news/page/1')


def get_posts(request, page):
    """
    Page where posts are displayed.
    """
    news = Publications.objects.all()
    if request.method == "POST": # Posts search
        search_text = request.POST.get("search_text")
        news = news.filter(title__icontains=search_text)
        search = True
        return render(request, 'news_list.html', {'news':news, "search":search, "search_text":search_text})
    search = False    
    news = Paginator(news, 10) # 10 posts per page.
    news = news.get_page(page)
    return render(request, 'news_list.html', {'news':news, "search":search})


def post(request, url):
    """
    Page where post is showed.
    """
    try:
        article = Publications.objects.get(slug=url)
        return render(request, 'news_post.html', {'post':article})
    except Exception as error:
        return render(request, 'error.html', {
            'title': "Статья не найдена",
            'error': "404",
            'description': "Статьи с таким именем не существует."
        })


@login_required(login_url="/login/")
@admin_only
def create_post(request):
    """
    Page where admin can create a new post.
    """
    if request.method == "POST":
        form = ArticleCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/news/')
    else:
        form = ArticleCreationForm()
        return render(request, 'news_editor.html', {'form':form})


@login_required(login_url="/login/")
@admin_only
def dashboard(request, page):
    """
    Dashboard for posts.
    """
    news = Publications.objects.all()
    news = Paginator(news, 100) # 100 posts per page
    news = news.get_page(page)
    return render(request, 'news_dashboard.html', {'news':news})


@login_required(login_url="/login/")
@admin_only
def dashboard_first(request):
    """
    Redirects user to the first page of the dashboard.
    """
    return redirect('/news/dashboard/1')


@login_required(login_url="/login/")
@admin_only
def news_delete(request, id):
    """
    Page where admin deletes a post.
    """
    article = Publications.objects.get(id=id)
    if request.method == "POST":
        article.delete()
        return redirect('/news/dashboard')
    context = {'item':article}
    return render(request, 'news_delete.html', context)


@login_required(login_url="/login/")
@admin_only
def news_update(request, id):
    """
    Page where post can be edited.
    """
    article = Publications.objects.get(id=id)
    # Oh shit, PyCharm, I'm sorry for overriding "id". 
    form = ArticleCreationForm(instance=article)
    if request.method == 'POST':
        form = ArticleCreationForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            if request.POST.get('deleteimage') is not None:
                article.image = ''
                article.save()
            return redirect('news_dashboard')
    context = {'form':form, 'data':article}
    return render(request, 'news_editor.html', context)