from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict
from rest_framework.decorators import api_view
from . import models, functions, serializer


@api_view(['POST'])
def diary_api(request):
    if request.user.is_authenticated and request.user.account_type == 3:
        student = models.Students.objects.get(account=request.user)
        grade = student.grade
        if grade is None:
            return Response(OrderedDict({
                'error': 403,
                'description': 'Student is not in class'
            }), status=status.HTTP_403_FORBIDDEN)
        try:
            chosen_quarter = request.data['term']
        except Exception:
            return Response(OrderedDict({
                'error': 400,
                'description': 'Bad form'
            }), status=status.HTTP_400_BAD_REQUEST)
        subjects = grade.subjects.all()
        all_marks = student.marks_set.filter(lesson__quarter=chosen_quarter)
        if not all_marks:
            return Response(OrderedDict({
                'error': 400,
                'description': 'No marks'
            }), status=status.HTTP_400_BAD_REQUEST)
        d = {}
        max_length, total_missed = 0, 0

        for s in subjects:
            marks = all_marks.filter(subject=s.id).order_by('lesson__date')
            if len(marks) > max_length:
                max_length = len(marks)

            n_amount = 0
            marks_list = []
            for i in marks:
                if i.lesson.control.weight != 100:
                    if i.amount != -1:
                        marks_list.append(i)
                    else:
                        n_amount += 1
            avg = functions.get_average(marks_list)[0]
            smart_avg = functions.get_smart_average(marks_list)
            d.update({s.name: {'avg': avg, 'smart_avg': smart_avg, 'mark list': list(marks.values())}})

            total_missed += n_amount

        student = list(models.Students.objects.filter(account=request.user).values())
        print(d)
        return Response(OrderedDict({
            'student': student,
            'marks': d,
            'max_length': max_length,
            'total_missed': total_missed,
            'term': chosen_quarter,
        }), status=status.HTTP_200_OK)
    else:
        return Response(OrderedDict({
            'error': 403,
            'description': 'Not authenticated as student'
        }), status=status.HTTP_403_FORBIDDEN)
