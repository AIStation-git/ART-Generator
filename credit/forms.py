from django import forms

class UpdateCreditForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}))
    credit = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter Credit'}))
