from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Publications
from django.db.models import Max
from django.http import HttpResponseRedirect


def redirect(request):
    return HttpResponseRedirect('/news/1')


def get_posts(request, page):
    POSTS_ON_PAGE = 15
    news = Publications.objects.all()
    amount = news.count()
    news = news[POSTS_ON_PAGE * (page - 1):POSTS_ON_PAGE * page]
    if amount is not None:
        amount = int(amount)
        amount = amount - (POSTS_ON_PAGE * page)
    else:
        amount = 0
    return render(request, 'news.html', {'pub': news, 'current':page, 'prev':page-1, 'next':page+1, 'amount':amount})

def post(request, url):
    try:
        article = Publications.objects.get(slug=url)
        return render(request, 'news_details.html', {'post':article})
    except:
        return render(request, 'error.html', {
            'title': "Статья не найдена",
            'error': "404",
            'description': "Статьи с таким именем не существует."
        })