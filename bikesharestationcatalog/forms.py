from django import forms


class ImageForm(forms.Form):
    imgfile = forms.ImageField(label='Select a file')
