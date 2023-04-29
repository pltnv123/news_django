from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import Post


class PostForm(forms.ModelForm):
    # условие проверки
    # description = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'categoryType',
                  # 'author',
                  'postCategory',
                  ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                _("Описание не должно быть идентично названию.")
            )

        return cleaned_data

    # Проверка конкретного поля
    def clean_name(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                _("Название должно начинаться с заглавной буквы")
            )
        return title



#       PostForm   ==

# class ProductForm(forms.Form):
#     name = forms.CharField(label='Name')
#     description = forms.CharField(label='Description')
#     quantity = forms.IntegerField(label='Quantity')
#     category = forms.ModelChoiceField(
#         label='Category', queryset=Category.objects.all(),
#     )
#     price = forms.FloatField(label='Price')