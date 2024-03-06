from django import forms

class PostForm(forms.Form):
    post_content = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":"5"}), max_length=1000)