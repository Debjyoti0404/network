from django import forms

class PostForm(forms.Form):
    post_content = forms.CharField(label="", widget=forms.Textarea(attrs={
        "rows":"5",
        "placeholder":"What's on your mind?",
        "class": "form-control",
        "style":"width: 100%;font-size:24px;border:none;",
        }), max_length=1000)