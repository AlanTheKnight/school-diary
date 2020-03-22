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
    return redirect('/news/page/1')


def get_posts(request, page):
    news = Publications.objects.all()
    news = Paginator(news, 15)
    page_object = news.get_page(page)
    return render(request, 'news.html', {'news':page_object})


def post(request, url):
    try:
        article = Publications.objects.get(slug=url)
        return render(request, 'news_details.html', {'post':article})
    except Exception as error:
        return render(request, 'error.html', {
            'title': "Статья не найдена",
            'error': "404",
            'description': "Статьи с таким именем не существует."
        })


@login_required(login_url="/login/")
@admin_only
def create_post(request):
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
    news = Publications.objects.all()
    news = Paginator(news, 100)
    news = news.get_page(page)
    return render(request, 'news_view.html', {'news':news})


@login_required(login_url="/login/")
@admin_only
def dashboard_first(request):
    return redirect('/news/dashboard/1')


@login_required(login_url="/login/")
@admin_only
def news_delete(request, id):
    article = Publications.objects.get(id=id)
    if request.method == "POST":
        article.delete()
        return redirect('/news/dashboard')
    context = {'item':article}
    return render(request, 'news_delete.html', context)


@login_required(login_url="/login/")
@admin_only
def news_update(request, id):
    article = Publications.objects.get(id=id)
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