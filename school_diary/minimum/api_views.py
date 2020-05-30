from collections import OrderedDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Documents
from .serializer import ValidSerializer


@api_view(['POST'])
def minimum_api(request):
    form = ValidSerializer(data=request.data)
    if form.is_valid():

        chosen_grade = request.data['grade']
        chosen_subject = request.data['subject']
        chosen_term = request.data['term']
        try:
            minimum = Documents.objects.filter(
                grade=chosen_grade, term=chosen_term, subject=chosen_subject)
            return Response(OrderedDict({'minimum': list(minimum.values())}), status=status.HTTP_200_OK)
        except:
            return Response(OrderedDict({
                'title': "Have Not File",
                'error': "404",
            }), status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(OrderedDict({
            'title': "Bad form",
            'error': "400",
        }), status=status.HTTP_400_BAD_REQUEST)