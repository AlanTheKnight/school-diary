from django import forms


TYPES = [
    (-1, "Любой"),
    (1, "Администратор"),
    (2, "Учитель"),
    (3, "Ученик"),
]


class FilterForm(forms.Form):
    usertype = forms.ChoiceField(
        choices=TYPES, required=True, label="Тип пользователя")
