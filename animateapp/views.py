from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView

from animateapp.forms import AnimateCreationForm
from animateapp.models import CropAni


class AnimateCreateView(CreateView):
    model = CropAni
    form_class = AnimateCreationForm
    template_name = 'animateapp/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('animateapp:ani', kwargs={'pk': self.object.user.pk})