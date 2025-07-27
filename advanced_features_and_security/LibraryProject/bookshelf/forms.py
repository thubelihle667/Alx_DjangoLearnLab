from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = ['title', 'author']

