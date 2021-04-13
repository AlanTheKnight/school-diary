from rest_framework import serializers
from apps.core import models


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Students
        exclude = ["account"]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teachers
        exclude = ["account"]


class ListUsersSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    teacher = TeacherSerializer()

    class Meta:
        model = models.Users
        fields = [
            "id", "account_type", "email", "first_name",
            "second_name", "surname", "registration_date",
            "last_login", "student", "teacher"
        ]
