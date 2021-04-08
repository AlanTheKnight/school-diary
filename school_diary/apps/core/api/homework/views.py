import django_filters
from rest_framework import (
    generics, exceptions, permissions, authentication, serializers
)

from apps.core import models


class ListHomeworkView(generics.ListAPIView):
    class HomeworkFilter(django_filters.FilterSet):
        date = django_filters.DateFromToRangeFilter("lesson__date")
        file = django_filters.BooleanFilter("h_file", lookup_expr="isnull")
        quarter = django_filters.NumberFilter("lesson__quarter")

        class Meta:
            model = models.Homework
            fields = ('date',)

    class HomeworkSerializer(serializers.ModelSerializer):
        class SubjectsSerializer(serializers.ModelSerializer):
            class Meta:
                model = models.Subjects
                fields = "__all__"

        class LessonSerializer(serializers.ModelSerializer):
            class Meta:
                model = models.Lessons
                fields = ["date", "theme"]

        subject = SubjectsSerializer(source="lesson.group.subject")
        lesson = LessonSerializer()

        class Meta:
            model = models.Homework
            fields = "__all__"

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = HomeworkFilter
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        klass = self.request.user.student.klass
        if klass is None:
            raise exceptions.NotFound(detail="Student must be added to a klass.")
        return models.Homework.objects.filter(lesson__group__klass=klass)
