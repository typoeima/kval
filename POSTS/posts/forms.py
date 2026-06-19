from django import forms
from .models import Post
from django.utils import timezone

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_at', 'views', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'published_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'views': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'published_at': 'Дата публикации',
            'views': 'Количество просмотров',
            'is_published': 'Опубликовать',
        }