from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict


class DiaryApi(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.account_type == 3:
            return Response(OrderedDict({
                'success': True
            }))
        else:
            return Response(OrderedDict({
                'success': False
            }))
