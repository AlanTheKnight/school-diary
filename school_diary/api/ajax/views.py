from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from diary.models import Marks, Students, Lessons
from diary.functions import get_marks_data


class SaveMark(APIView):
    def post(self, request):
        data = request.POST
        print(data['name'])
        student_lesson_ids = data['name'].split('|')
        student_id, lesson_id = int(student_lesson_ids[0]), int(student_lesson_ids[1])
        student = Students.objects.get(pk=student_id)
        lesson = Lessons.objects.get(pk=lesson_id)
        subject = lesson.subject
        term = lesson.quarter

        # SAVE MARK
        if data['value']:
            value = int(data['value'])
            mark = Marks.objects.get_or_create(student=student, lesson=lesson, subject=subject)[0]
            mark.amount = value
            mark.save()
        else:
            mark = Marks.objects.get_or_create(student=student, lesson=lesson, subject=subject)[0]
            mark.delete()

        #     MAKE RESPONSE
        marks = student.marks_set.filter(subject=subject, lesson__quarter=term)
        try:
            sm_avg, avg, _, _, _, _ = get_marks_data(marks)
        except ZeroDivisionError:
            sm_avg = avg = '-'
        data = {
            "id": str(student.pk),
            "sm_avg": sm_avg,
            "avg": avg
        }
        return Response(data, status=status.HTTP_200_OK)
