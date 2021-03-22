from rest_framework import serializers
from . import models
from apps.core import models as core_models


class BasicUserSerializer(serializers.ModelSerializer):
    klass = serializers.CharField(source="student.klass")

    class Meta:
        model = core_models.Users
        fields = ["first_name", "second_name", "surname", "email", "klass"]


class ListCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = "__all__"


class NotesGroupSerializer(serializers.ModelSerializer):
    author = BasicUserSerializer()
    files_size = serializers.IntegerField()
    thumbnail = serializers.ImageField(allow_null=True)

    class Meta:
        model = models.NotesGroup
        fields = "__all__"


class NotesGroupDetailsSerializer(serializers.ModelSerializer):
    author = BasicUserSerializer()
    files_size = serializers.IntegerField()
    notes = NoteSerializer(many=True)

    class Meta:
        model = models.NotesGroup
        fields = "__all__"

