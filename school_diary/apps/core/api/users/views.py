from rest_framework import views, generics, permissions, authentication
from . import serializers
from apps.core import models
import django_filters


class ListUsersView(generics.ListAPIView):
    class UsersFilter(django_filters.FilterSet):
        account_type = django_filters.MultipleChoiceFilter("account_type", choices=(
            (0, "root"), (1, "admin"), (2, "teacher"), (3, "student")
        ))

        class Meta:
            model = models.Users
            fields = []

    queryset = models.Users.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
    serializer_class = serializers.ListUsersSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = UsersFilter


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.ListUsersSerializer
    authentication_classes = [authentication.SessionAuthentication]
    queryset = models.Users.objects.all()


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = serializers.ListUsersSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Users.objects.all()

    def get_object(self):
        return self.request.user
