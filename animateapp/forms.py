from django.forms import ModelForm, HiddenInput

from animateapp.custom_widgets import PreviewImageFileWidget
from animateapp.models import Animate


class AnimateCreationForm(ModelForm):
    class Meta:
        model = Animate
        fields = ['image', 'ani']
        widgets = {
            #'image': PreviewImageFileWidget(),
            'ani': HiddenInput(),
        }

        