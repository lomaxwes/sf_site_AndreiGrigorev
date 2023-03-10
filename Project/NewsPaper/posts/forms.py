from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'content']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        title = cleaned_data.get("title")
        if title == content:
            raise ValidationError("Описание не должно быть идентично названию.")
        return cleaned_data
