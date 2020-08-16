from rest_framework import generics
from diary import models
from api import permissions
from . import serializers


class GradesList(generics.ListAPIView):
    queryset = models.Grades.objects.all()
    serializer_class = serializers.GradeListSerializer


class GradesDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Grades.objects.all()
    serializer_class = serializers.GradeDetailsSerializer
    permission_classes = [permissions.APIUserPermission]
