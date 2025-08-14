from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        def __init__(self, *args, **kwargs):
            super(PostForm,self).__init__(*args, **kwargs)
            self.fields['title'].widget.attrs['placeholder'] = 'Enter post title'
            self.fields['content'].widget.attrs['placeholder'] = 'Enter post content'
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write a comment...'}),
        }

        def clean_content(self):
            content = self.clean_data.get('content')
            if not content:
                raise forms.ValidationError('Comment content is required.')
            if len(content) > 1000:
                raise forms.ValidationError('Comment is too long. Maximum 1000 characters.')
            return content