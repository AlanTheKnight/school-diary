from rest_framework import serializers
from diary import models


class SaveMarkSerializer(serializers.Serializer):
    value = serializers.IntegerField(
        required=True, min_value=-1, max_value=5)
    student = serializers.IntegerField(required=True)
    lesson = serializers.IntegerField(required=True)


class AddCommentSerializer(serializers.Serializer):
    student = serializers.IntegerField(required=True)
    lesson = serializers.IntegerField(required=True)
    comment = serializers.CharField(required=True, max_length=400)


class GetCommentSerializer(serializers.Serializer):
    student = serializers.IntegerField(required=True)
    lesson = serializers.IntegerField(required=True)


class LessonsListSerializer(serializers.ModelSerializer):
    control_name = serializers.CharField(source="control.name")

    class Meta:
        model = models.Lessons
        fields = '__all__'


class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Controls
        exclude = ('weight', )
