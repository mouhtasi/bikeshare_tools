from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, validate_image_file_extension


def file_size(value):
    limit = 20 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 20 MiB.')


class ImageForm(forms.Form):
    imgfile = forms.ImageField(label='Upload an image for this station:', validators=[file_size, FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png', 'heif']), validate_image_file_extension],
                               widget=forms.FileInput(attrs={'accept': '.jpg, .jpeg, .png, .heic'}))
