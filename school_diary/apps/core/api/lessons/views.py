from rest_framework import (
    generics, authentication, serializers
)

from .. import permissions
from ... import models


class LessonsList(generics.ListAPIView):
    class LessonsListSerializer(serializers.ModelSerializer):
        control_name = serializers.CharField(source="control.name")

        class Meta:
            model = models.Lessons
            fields = '__all__'

    authentication_classes = (authentication.SessionAuthentication,)
    serializer_class = LessonsListSerializer
    permission_classes = (permissions.InBuiltAPIPermission,)

    def get_queryset(self):
        group_id = self.request.GET['group']
        term = self.request.GET['quarter']
        return models.Lessons.objects.filter(group_id=group_id, quarter=term)


class EditLesson(generics.RetrieveUpdateDestroyAPIView):
    class EditLessonSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Lessons
            fields = '__all__'

    queryset = models.Lessons.objects.all()
    serializer_class = EditLessonSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.BasicAuthentication)
