from rest_framework import generics
from core import models
from core.api import permissions
from . import serializers


class GradesList(generics.ListAPIView):
    queryset = models.Klasses.objects.all()
    serializer_class = serializers.GradeListSerializer


class GradesDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Klasses.objects.all()
    serializer_class = serializers.GradeDetailsSerializer
    permission_classes = [permissions.APIUserPermission]
