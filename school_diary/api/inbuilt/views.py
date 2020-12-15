from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework import generics
from diary import models
from diary.functions import get_marks_data
from django.shortcuts import get_object_or_404
from . import serializers
from api import permissions


class SaveMark(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def post(self, request):
        if not (request.user.is_authenticated and request.user.account_type) == 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.SaveMarkSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        student = models.Students.objects.get(pk=serializer.validated_data['student'])
        lesson = models.Lessons.objects.get(pk=serializer.validated_data['lesson'])
        group = lesson.group
        term = lesson.quarter

        value = int(serializer.validated_data['value'])
        mark = models.Marks.objects.get_or_create(student=student, lesson=lesson)[0]
        if value != 0:  # Otherwise we need to delete mark
            mark.amount = value
            mark.save()
        else:
            mark.delete()

        marks = student.marks_set.filter(lesson__group=group, lesson__quarter=term)
        sm_avg, avg, *_ = get_marks_data(marks)
        data = {
            "pk": str(student.pk),
            "sm_avg": sm_avg,
            "avg": avg
        }
        return Response(data, status=status.HTTP_200_OK)


class AddComment(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def post(self, request):
        if not (request.user.is_authenticated and request.user.account_type) == 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.AddCommentSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        try:
            mark = models.Marks.objects.get(
                student_id=serializer.validated_data['student'],
                lesson_id=serializer.validated_data['lesson']
            )
            mark.comment = serializer.validated_data['comment']
            mark.save()
            data = {"status": "success"}
        except models.Marks.DoesNotExist:
            data = {"status": "aborted"}
        return Response(data, status=status.HTTP_200_OK)


class GetCommentText(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def post(self, request):
        if not (request.user.is_authenticated and request.user.account_type) == 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.GetCommentSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        try:
            mark = models.Marks.objects.get(
                student_id=serializer.validated_data['student'],
                lesson_id=serializer.validated_data['lesson']
            )
            data = {"status": "success", "comment": mark.comment}
        except models.Marks.DoesNotExist:
            data = {"status": "aborted"}
        return Response(data, status=status.HTTP_200_OK)


class LessonsList(generics.ListAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    serializer_class = serializers.LessonsListSerializer
    permission_classes = (permissions.InBuiltAPIPermission,)

    def get_queryset(self):
        group_id = self.request.GET['group']
        term = self.request.GET['term']
        return models.Lessons.objects.filter(group_id=group_id, quarter=term)


class ListControls(generics.ListAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    serializer_class = serializers.ControlSerializer
    permission_classes = (permissions.InBuiltAPIPermission,)
    queryset = models.Controls.objects.all()


class ChangeLessonIsPlanned(APIView):
    authentication_classes = (authentication.SessionAuthentication, )

    def post(self, request):
        if not (request.user.is_authenticated and request.user.account_type) == 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ChangeLessonIsPlannedSerializer(
            data=request.POST
        )
        serializer.is_valid(raise_exception=True)
        lesson = get_object_or_404(
            models.Lessons,
            pk=serializer.validated_data['lesson']
        )
        lesson.is_plan = not lesson.is_plan
        lesson.save()
        return Response(status=status.HTTP_200_OK)


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
