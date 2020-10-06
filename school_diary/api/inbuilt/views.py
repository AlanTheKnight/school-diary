from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from diary.models import Marks, Students, Lessons
from diary.functions import get_marks_data
from . import serializers


class SaveMark(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def post(self, request):
        if not (request.user.is_authenticated and request.user.account_type) == 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.SaveMarkSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        student = Students.objects.get(pk=serializer.validated_data['student'])
        lesson = Lessons.objects.get(pk=serializer.validated_data['lesson'])
        group = lesson.group
        term = lesson.quarter

        value = int(serializer.validated_data['value'])
        mark = Marks.objects.get_or_create(student=student, lesson=lesson)[0]
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
        mark = Marks.objects.get(pk=serializer.validated_data['mark'])
        mark.comment = serializer.validated_data['comment']
        mark.save()
        return Response(status=status.HTTP_200_OK)


class GetCommentText(APIView):
    authentication_classes = (authentication.SessionAuthentication,)

    def post(self, request):
        if not (request.user.is_authenticated and request.user.account_type) == 2:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.GetCommentSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        mark = Marks.objects.get(pk=serializer.validated_data['mark'])
        data = {"comment": mark.comment}
        return Response(data, status=status.HTTP_200_OK)
