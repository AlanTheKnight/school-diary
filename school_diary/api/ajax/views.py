from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from diary.models import Marks, Students, Lessons
from diary.functions import get_marks_data


class SaveMark(APIView):
    def post(self, request):
        if request.user.is_authenticated and request.user.account_type == 2:
            data = request.POST
            student_lesson_ids = data['name'].split('|')
            student_id, lesson_id = int(student_lesson_ids[0]), int(student_lesson_ids[1])
            student = Students.objects.get(pk=student_id)
            lesson = Lessons.objects.get(pk=lesson_id)
            group = lesson.group
            term = lesson.quarter

            # SAVE MARK_, _, _, _
            if data['value']:
                value = None if data['value'] == "" else int(data['value'])
                mark = Marks.objects.get_or_create(student=student, lesson=lesson)[0]
                mark.amount = value
                mark.save()
            else:
                mark = Marks.objects.get_or_create(student=student, lesson=lesson)[0]
                mark.delete()

            #     MAKE RESPONSE
            marks = student.marks_set.filter(lesson__group=group, lesson__quarter=term)
            avg, sm_avg, *_ = get_marks_data(marks)
            data = {
                "pk": str(student.pk),
                "sm_avg": sm_avg,
                "avg": avg
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

