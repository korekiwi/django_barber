from django import forms

from core.models import Visit, Review


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ["name", "phone", "comment", "master", "services"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form_control", "placeholder": "Имя"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form_control", "placeholder": "Телефон"}
            ),
            "comment": forms.Textarea(
                attrs={"class": "form_control", "placeholder": "Комментарий"}
            ),
            "master": forms.Select(attrs={"class": "form_control", "placeholder": "Мастер"}),
            "services": forms.SelectMultiple(attrs={"class": "form_control"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "text", "master", "rating"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form_control", "placeholder": "Имя"}
            ),
            "text": forms.Textarea(
                attrs={"class": "form_control", "placeholder": "Комментарий"}
            ),
            "master": forms.Select(attrs={"class": "form_control", "placeholder": "Мастер"}),
            "rating": forms.Select(attrs={"class": "form_control", "placeholder": "Рейтинг"})
        }
