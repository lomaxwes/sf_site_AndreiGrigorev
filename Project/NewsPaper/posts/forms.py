from django import forms
from django.contrib.auth.models import User

from .models import Post, Category
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=20)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

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
