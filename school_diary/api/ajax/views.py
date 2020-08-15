from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from diary.models import Marks, Students, Lessons


class SaveMark(APIView):
    def post(self, request):
        data = request.POST
        student_lesson_ids = data['name'][5:].split('|')
        student_id, lesson_id = int(student_lesson_ids[0]), int(student_lesson_ids[1])
        value = int(data['value'])
        student = Students.objects.get(pk=student_id)
        lesson = Lessons.objects.get(pk=lesson_id)
        mark = Marks.objects.get_or_create(student=student, lesson=lesson)[0]
        mark.amount = value
        mark.save()
        return Response(status=status.HTTP_200_OK)
