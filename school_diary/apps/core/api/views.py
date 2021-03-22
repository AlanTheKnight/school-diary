from rest_framework import status, authentication, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, permissions
from .. import models


class SaveMark(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def post(self, request):
        if not (request.user.is_authenticated and request.user.account_type) == 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.SaveMarkSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        student = models.Students.objects.get(
            pk=serializer.validated_data['student'])
        lesson = models.Lessons.objects.get(
            pk=serializer.validated_data['lesson'])
        term = lesson.quarter

        value = int(serializer.validated_data['value'])
        grade = models.Grades.objects.get_or_create(
            student=student, lesson=lesson)[0]
        if value != 0:  # Otherwise we need to delete mark
            grade.amount = value
            grade.save()
        else:
            grade.delete()

        grades = student.grades_set.filter(
            lesson__group=lesson.group, lesson__quarter=term)
        grades_data = models.Grades.get_data(grades)
        data = {
            "pk": str(student.pk),
            "sm_avg": grades_data["sm_avg"],
            "avg": grades_data["avg"]
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
            mark = models.Grades.objects.get(
                student_id=serializer.validated_data['student'],
                lesson_id=serializer.validated_data['lesson']
            )
            mark.comment = serializer.validated_data['comment']
            mark.save()
            data = {"status": "success"}
        except models.Grades.DoesNotExist:
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
            mark = models.Grades.objects.get(
                student_id=serializer.validated_data['student'],
                lesson_id=serializer.validated_data['lesson']
            )
            data = {"status": "success", "comment": mark.comment}
        except models.Grades.DoesNotExist:
            data = {"status": "aborted"}
        return Response(data, status=status.HTTP_200_OK)


class ListControls(generics.ListAPIView):
    authentication_classes = (authentication.SessionAuthentication,)
    serializer_class = serializers.ControlSerializer
    permission_classes = (permissions.InBuiltAPIPermission,)
    queryset = models.Controls.objects.all()
