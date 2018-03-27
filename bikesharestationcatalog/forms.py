from django import forms


class ImageForm(forms.Form):
    imgfile = forms.ImageField(label='Upload an image for this station:')
