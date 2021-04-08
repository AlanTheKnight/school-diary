from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import (
    views, response, generics, serializers
)

from . import serializers as local_serializers
from ... import models


class ListStudentGrades(views.APIView):
    def post(self, request):
        serializer = local_serializers.ListStudentGradesSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        group: models.Groups = get_object_or_404(
            models.Groups, pk=serializer.validated_data['group'])
        table = group.get_table(quarter=serializer.validated_data['quarter'])
        data = local_serializers.StudentGradesResponseSerializer(table).data
        return response.Response(data)


class GetOrCreateGroupAPI(views.APIView):
    def post(self, request):
        serializer = local_serializers.GetGroupSerializer(
            data=request.POST
        )
        serializer.is_valid(raise_exception=True)
        group = models.Groups.create_group(
            klass_id=serializer.validated_data['klass_id'],
            subject_id=serializer.validated_data['subject_id']
        )
        data = local_serializers.GroupSerializer(group).data
        return response.Response(data)


class Grade(generics.RetrieveUpdateDestroyAPIView):
    class GradeSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Grades
            fields = "__all__"

    serializer_class = GradeSerializer
    queryset = models.Grades.objects.all()

    def get_object(self):
        queryset: QuerySet[models.Grades] = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            student_id=self.request.GET['student'],
            lesson_id=self.request.GET['lesson'])
        self.check_object_permissions(self.request, obj)
        return obj
