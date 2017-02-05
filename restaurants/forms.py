from django import forms

class CommentForm(forms.Form):
    visitor = forms.CharField()
    email = forms.EmailField(required=False)
    content = forms.CharField()
    # visitor = forms.CharField(max_length=20, widget=forms.TextInput())
    # email = forms.EmailField(max_length=20, widget=forms.TextInput(), required=False)
    # content = forms.CharField(max_length=200, widget=forms.Textarea())
