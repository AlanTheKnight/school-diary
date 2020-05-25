from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict
from rest_framework.decorators import api_view
from . import models, functions, serializer


@api_view(['GET'])
def diary_api(request, term):
    if request.user.is_authenticated and request.user.account_type == 3:
        student = models.Students.objects.get(account=request.user)
        grade = student.grade
        if grade is None:
            return Response(OrderedDict({
                'error': 403,
                'description': 'Student is not in class'
            }), status=status.HTTP_403_FORBIDDEN)
        chosen_quarter = term
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
            mark_list = list(marks.values())
            d.update({s.name: {'avg': avg, 'smart_avg': smart_avg, 'mark list': mark_list}})

            total_missed += n_amount

        student = list(models.Students.objects.filter(account=request.user).values())[0]
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


@api_view(['GET'])
def get_student(request, pk):
    student = models.Students.objects.filter(pk=pk)
    if student:
        return Response(OrderedDict({
            'student': list(student.values())[0]
        }))
    else:
        return Response(OrderedDict({
            'error': 404,
            'description': 'No student'
        }), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_lesson(request, pk):
    lesson = models.Lessons.objects.filter(pk=pk)
    if lesson:
        return Response(OrderedDict({
            'lesson': list(lesson.values())[0]
        }))
    else:
        return Response(OrderedDict({
            'error': 404,
            'description': 'No lesson'
        }), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_grade(request, pk):
    grade = models.Grades.objects.filter(pk=pk)
    if grade:
        return Response(OrderedDict({
            'grade': list(grade.values())[0]
        }))
    else:
        return Response(OrderedDict({
            'error': 404,
            'description': 'No grade'
        }), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_subject(request, pk):
    subject = models.Grades.objects.filter(pk=pk)
    if subject:
        return Response(OrderedDict({
            'grade': list(subject.values())[0]
        }))
    else:
        return Response(OrderedDict({
            'error': 404,
            'description': 'No grade'
        }), status=status.HTTP_404_NOT_FOUND)