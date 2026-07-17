from django import forms
from .models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'is_published']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 300px; resize: vertical;'
            }),

            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),

            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }