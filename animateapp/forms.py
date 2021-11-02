from django.forms import ModelForm, forms

from animateapp.models import CropAni


class AnimateCreationForm(ModelForm):
    class Meta:
        model = CropAni
        fields = ['image']
        widgets = {
            'image': forms.FileField(attrs={'onchages':''})
        }

        