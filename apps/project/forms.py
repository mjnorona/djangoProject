from django import forms
from models import Document

class ProfileImageForm(forms.Form):
    image = forms.FileField(label='Select a profile Image')

