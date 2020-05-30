from collections import OrderedDict

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serialazer import ValidSerializer
from .models import Publications


@api_view(['GET'])
def post_api(request, url):
    """
    Page where post is showed.
    """
    try:
        article = Publications.objects.filter(slug=url)
        return Response(OrderedDict({
            'post': list(article.values())
        }), status=status.HTTP_200_OK)
    except Exception:
        return Response(OrderedDict({
            'title': "Статья не найдена",
            'error': "404",
        }), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def get_posts_api(request):
    news = Publications.objects.all()
    if request.method == 'POST':
        form = ValidSerializer(data=request.data)
        if form.is_valid():
            data = request.data
            search_text = data.get("search_text")
            news = news.filter(title__icontains=search_text)
            search = True
            context = OrderedDict({
                'news': list(news.values()),
                'search': search,
                'search_text': search_text
            })
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(OrderedDict({
                'title': "Bad form",
                'error': "400",
            }), status=status.HTTP_400_BAD_REQUEST)
    else:
        context = OrderedDict({
            'news': list(news.values()),
            'search': False
        })
        return Response(context, status=status.HTTP_200_OK)