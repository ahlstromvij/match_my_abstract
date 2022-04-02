from django import forms

class AbstractForm(forms.Form):
    user_abstract = forms.CharField(label='Your abstract', max_length=500)