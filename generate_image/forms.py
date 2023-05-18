from django import forms

class UpdateCreditForm(forms.Form):
    email = forms.EmailField()
    credit = forms.CharField(max_length=150)
