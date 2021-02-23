from django.db.models import Q
from rest_framework import generics, authentication, views, response, parsers

from . import models, serializers


class ListCategories(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.ListCategoriesSerializer
    authentication_classes = [authentication.SessionAuthentication]


class ListNotesGroups(generics.ListAPIView):
    serializer_class = serializers.NotesGroupSerializer
    authentication_classes = [authentication.SessionAuthentication]

    def get_queryset(self):
        user_klass = self.request.user.student.klass
        qs = models.NotesGroup.objects.filter(
            Q(author__student__klass=user_klass) | Q(public=True),
        ).order_by("-upload_date")
        return qs


class ListMyNotesGroups(generics.ListAPIView):
    serializer_class = serializers.NotesGroupSerializer
    authentication_classes = [authentication.SessionAuthentication]

    def get_queryset(self):
        return models.NotesGroup.objects.filter(author=self.request.user).order_by("-upload_date")


class NoteGroupDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.NotesGroupDetailsSerializer
    authentication_classes = [authentication.SessionAuthentication]
    queryset = models.NotesGroup.objects.all()


class UploadNoteView(views.APIView):
    authentication_classes = [authentication.SessionAuthentication]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def post(self, request):
        files = request.FILES.getlist("files")
        group: int = int(request.POST.get("group"))

        enhance_photo = request.POST.get('filterPhoto') is not None

        for file in files:
            instance = models.Note(group_id=group, image=file)
            if not instance.save(enhance_image=enhance_photo):
                return response.Response(status=415)

        return response.Response()


class DeleteNoteView(generics.DestroyAPIView):
    serializer_class = serializers.NoteSerializer
    authentication_classes = [authentication.SessionAuthentication]
    queryset = models.Note.objects.all()
