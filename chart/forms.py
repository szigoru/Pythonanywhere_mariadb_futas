
# import form class from django
from django import forms
  
# import GeeksModel from models.py
from .models import Futasok
  
# create a ModelForm
class Futasokform(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Futasok
        exclude = ['id']