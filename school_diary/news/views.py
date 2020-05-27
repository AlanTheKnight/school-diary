from django.shortcuts import render, redirect, get_object_or_404
from .models import Publications
from django.core.paginator import Paginator


def first_page(request):
    """Redirects user to the first page of news feed."""
    return redirect('news', page=1)


def get_posts(request, page):
    """Page where posts are displayed."""
    news = Publications.objects.all()
    if request.method == "POST":  # Posts search
        search_text = request.POST.get("search_text")
        news = news.filter(title__icontains=search_text)
        search = True
        context = {'news': news, "search": search, "search_text": search_text}
        return render(request, 'news_list.html', context)
    search = False
    news = Paginator(news, 10)  # 10 posts per page.
    news = news.get_page(page)
    return render(request, 'news_list.html', {'news': news, "search": search})

  
def post(request, url):
    """Page where post is showed."""
    article = get_object_or_404(Publications, slug=url)
    return render(request, 'news_post.html', {'post': article})
