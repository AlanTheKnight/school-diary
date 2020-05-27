from rest_framework import serializers
from .models import Subjects, Students


class SubjectSerializer(serializers.ModelSerializer):
    class Meta():
        model = Subjects


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
{"term":4}
