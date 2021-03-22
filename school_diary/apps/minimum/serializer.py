from rest_framework import serializers


class ValidSerializer(serializers.Serializer):
    subject = serializers.ChoiceField(choices=[
        ("Информатика", "Информатика"),
        ("История", "История"),
        ("Литература", "Литература"),
        ("Математика", "Математика"),
        ("Обществознание", "Обществознание"),
        ("Русский язык", "Русский язык"),
        ("Химия и биология", "Хим-Био"),
        ("Экономика", "Экономика"),
        ("Физика", "Физика")])
    grade = serializers.ChoiceField(choices=[
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11)])
    term = serializers.ChoiceField(choices=[
        (1, "I"),
        (2, "II"),
        (3, "III"),
        (4, "IV")])

# {"subject": "Информатика",
# "grade": 8,
# "term": 4}
