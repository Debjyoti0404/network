from django import forms

class PostForm(forms.Form):
    post_content = forms.CharField(label="New Post", max_length=1000)

class CommentForm(forms.Form):
    comment_content = forms.CharField(max_length=1000)