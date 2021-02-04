from rest_framework import serializers
from core import models


class LessonsListSerializer(serializers.ModelSerializer):
    control_name = serializers.CharField(source="control.name")

    class Meta:
        model = models.Lessons
        fields = '__all__'


class ChangeLessonIsPlannedSerializer(serializers.Serializer):
    lesson = serializers.IntegerField(required=True)


class EditLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lessons
        fields = '__all__'


class ListStudentGradesSerializer(serializers.Serializer):
    quarter = serializers.IntegerField(required=True)
    group = serializers.IntegerField(required=True)


class GradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Grades
        fields = ("amount", "lesson_id")


class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="account.first_name")
    second_name = serializers.CharField(source="account.second_name")
    surname = serializers.CharField(source="account.surname")

    class Meta:
        model = models.Students
        fields = ("first_name", "second_name", "surname", "pk")


class ScopeSerializer(serializers.Serializer):
    student = StudentSerializer()
    avg = serializers.FloatField(allow_null=True)
    sm_avg = serializers.FloatField(allow_null=True)
    grades = GradesSerializer(many=True)


class TableLessonsSerializer(serializers.ModelSerializer):
    control_name = serializers.CharField(source="control.name")

    class Meta:
        model = models.Lessons
        fields = ('date', 'theme', 'control_name', "id")


class StudentGradesResponseSerializer(serializers.Serializer):
    lessons = TableLessonsSerializer(many=True)
    scope = ScopeSerializer(many=True)


class GetGroupSerializer(serializers.Serializer):
    subject_id = serializers.IntegerField(required=True)
    klass_id = serializers.IntegerField(required=True)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Groups
        fields = '__all__'


class RetrieveLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lessons
        fields = '__all__'

