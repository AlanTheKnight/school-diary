from django.shortcuts import get_object_or_404
from rest_framework import (
    generics, authentication, views,
    status, response
)

from . import serializers
from .. import permissions
from ... import models


class LessonsList(generics.ListAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    serializer_class = serializers.LessonsListSerializer
    permission_classes = (permissions.InBuiltAPIPermission,)

    def get_queryset(self):
        group_id = self.request.GET['group']
        term = self.request.GET['term']
        return models.Lessons.objects.filter(group_id=group_id, quarter=term)


class EditLesson(generics.UpdateAPIView):
    queryset = models.Lessons.objects.all()
    serializer_class = serializers.EditLessonSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.BasicAuthentication)


class DeleteLesson(generics.DestroyAPIView):
    queryset = models.Lessons.objects.all()
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.BasicAuthentication)


class ChangeLessonIsPlanned(views.APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def post(self, request):
        if not (request.user.is_authenticated and request.user.account_type) == 2:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ChangeLessonIsPlannedSerializer(
            data=request.POST
        )
        serializer.is_valid(raise_exception=True)
        lesson: models.Lessons = get_object_or_404(
            models.Lessons,
            pk=serializer.validated_data['lesson']
        )
        lesson.is_planned = not lesson.is_planned
        lesson.save()
        return response.Response(status=status.HTTP_200_OK)


class ListStudentGrades(views.APIView):
    def post(self, request):
        serializer = serializers.ListStudentGradesSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        group: models.Groups = get_object_or_404(
            models.Groups, pk=serializer.validated_data['group'])
        table = group.get_table(quarter=serializer.validated_data['quarter'])
        data = serializers.StudentGradesResponseSerializer(table).data
        return response.Response(data)


class GetOrCreateGroupAPI(views.APIView):
    def post(self, request):
        serializer = serializers.GetGroupSerializer(
            data=request.POST
        )
        serializer.is_valid(raise_exception=True)
        group = models.Groups.create_group(
            klass_id=serializer.validated_data['klass_id'],
            subject_id=serializer.validated_data['subject_id']
        )
        data = serializers.GroupSerializer(group).data
        return response.Response(data)


class RetrieveLesson(generics.RetrieveAPIView):
    queryset = models.Lessons.objects.all()
    serializer_class = serializers.RetrieveLessonSerializer
