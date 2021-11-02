from django.forms import ModelForm, forms

from animateapp.custom_widgets import PreviewImageFileWidget
from animateapp.models import CropAni


class AnimateCreationForm(ModelForm):
    class Meta:
        model = CropAni
        fields = ['image']
        #widgets = {
        #    'image': PreviewImageFileWidget()
        #}

        