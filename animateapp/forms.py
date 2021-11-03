from django.forms import ModelForm, forms, FileInput, HiddenInput

from animateapp.custom_widgets import PreviewImageFileWidget
from animateapp.models import Animate


class AnimateCreationForm(ModelForm):
    class Meta:
        model = Animate
        fields = ['image', 'ani']
        widgets = {
            #'ani': PreviewImageFileWidget(),
            'ani': HiddenInput(attrs={
                'class': "form-control p-1",
                'id': 'ani',
                'style': ""
            }),
        }

        