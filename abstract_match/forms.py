from django import forms

class AbstractForm(forms.Form):
    user_abstract = forms.CharField(widget=forms.Textarea, label='')