from django import forms

class UploadSpectStructForm(forms.Form):
    inputSpectrum = forms.FileField(required=True)
    inputStructure = forms.FileField(required=True)
