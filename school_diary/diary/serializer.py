from rest_framework import serializers
from .models import Subjects


class SubjectSerializer(serializers.Serializer):
    class Meta():
        model = Subjects