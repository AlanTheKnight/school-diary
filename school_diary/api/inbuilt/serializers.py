from rest_framework import serializers


class SaveMarkSerializer(serializers.Serializer):
    value = serializers.IntegerField(
        required=True, min_value=-1, max_value=5)
    student = serializers.IntegerField(required=True)
    lesson = serializers.IntegerField(required=True)


class AddCommentSerializer(serializers.Serializer):
    student = serializers.IntegerField(required=True)
    lesson = serializers.IntegerField(required=True)
    comment = serializers.CharField(required=True, max_length=400)


class GetCommentSerializer(serializers.Serializer):
    student = serializers.IntegerField(required=True)
    lesson = serializers.IntegerField(required=True)
