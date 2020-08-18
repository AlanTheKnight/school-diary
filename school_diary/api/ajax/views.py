from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from diary.models import Marks, Students, Lessons


class SaveMark(APIView):
    def post(self, request):
        data = request.POST
        print(data['name'])
        student_lesson_ids = data['name'][5:].split('|')
        student_id, lesson_id = int(student_lesson_ids[0]), int(student_lesson_ids[1])
        student = Students.objects.get(pk=student_id)
        lesson = Lessons.objects.get(pk=lesson_id)
        subject = lesson.subject
        if data['value']:
            value = int(data['value'])
            mark = Marks.objects.get_or_create(student=student, lesson=lesson, subject=subject)[0]
            mark.amount = value
            mark.save()
        else:
            mark = Marks.objects.get_or_create(student=student, lesson=lesson, subject=subject)[0]
            mark.delete()
        return Response(status=status.HTTP_200_OK)
