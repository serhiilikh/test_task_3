from django import forms
from core.models import Post


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
