from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView

from animateapp.forms import AnimateCreationForm
from animateapp.models import CropAni

from PIL import Image
import pytesseract
import argparse
import cv2
import os


class AnimateCreateView(CreateView):
    model = CropAni
    form_class = AnimateCreationForm
    template_name = 'animateapp/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('animateapp:ani', kwargs={'pk': self.object.user.pk})


# 영어 인식
#print(pytesseract.image_to_string(Image.open('english.png')))

# 한글
#print(pytesseract.image_to_string(Image.open('hangul.png'), lang='Hangul'))



# load the example image and convert it to grayscale
#image = cv2.imread("test.png")
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
#filename = "{}.png".format(os.getpid())
#cv2.imwrite(filename, gray)

#pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

#text = pytesseract.image_to_string(Image.open(filename))
#os.remove(filename)

#print(text)