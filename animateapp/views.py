import datetime

from django.core.files.storage import FileSystemStorage
from django.http import FileResponse

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView
from django.views.generic.detail import SingleObjectMixin

from animateapp.forms import AnimateCreationForm
from animateapp.models import Animate

from PIL import Image
import pytesseract
import cv2.cv2 as cv2
import os

pytesseract.pytesseract.tesseract_cmd = R'C:\Django\lib\Tesseract-OCR\tesseract'


class AnimateCreateView(CreateView):
    model = Animate
    form_class = AnimateCreationForm
    template_name = 'animateapp/create.html'

    def form_valid(self, form):
        temp_upload = form.save(commit=False)
        temp_upload.save()
        temp_upload = form.save(commit=False)
        path = 'media/' + str(temp_upload.image)

        #이미지 컷 분류해서 순서에 맞춰 컷 나누기
        #임시 이미지 분할
        image_len_list = crop(path)

        #이미지와 길이를 가져와 순서대로 영상화
        video, video_path = view_seconds(image_len_list)
        temp_upload.ani = video_path
        temp_upload.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('animateapp:detail', kwargs={'pk': self.object.pk})


class AnimateDetailView(DetailView):
    model = Animate
    context_object_name = 'target_animate'
    template_name = 'animateapp/detail.html'


class FileDownloadView(SingleObjectMixin, View):
    #queryset = Animate.objects.all()
    def get(self, request, pk):
        object = self.get_object(pk)
        file_path = object.ani.path
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={object.get_filename()}'

        return response


# def download(request, id):
#  file_info = FileInfo.objects.get(id=id)
#  print('      ：' + file_info.file_name)
#  file = open(file_info.file_path, 'rb')
#  response = FileResponse(file)
#  response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(file_info.file_name)
#  return response


#임시로 이미지 분할
def crop(path):
    im = Image.open(path)
    img_width, img_height = im.size

    src = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    hei_3 = int(img_height / 3)
    crop_img = []
    # 이미지를 자른다.
    for i in range(3):
        dst = src[hei_3*i:hei_3*(i+1):, 0:img_width].copy()
        txt_len = img_text_len(dst)
        crop_img.append([i, dst, txt_len])
    return crop_img


def img_text_len(img):
    out_text = pytesseract.image_to_string(img, lang='kor+eng', config='--psm 1 -c preserve_interword_spaces=1')
    print("길이:"+str(len(out_text)))
    print(out_text)
    return len(out_text)


def view_seconds(image_list):
    nowdate = datetime.datetime.now()
    daytime = nowdate.strftime("%Y-%m-%d_%H%M%S")
    video_name = 'ani/'+daytime+'.mp4'
    out_path = 'media/' + video_name
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # define the video codec

    frame = image_list[0][1]
    height, width, layers = frame.shape

    video = cv2.VideoWriter(out_path, fourcc, 1.0, (width, height))
    for image in image_list:
        each_image_duration = 5 + int(image[2]/10)
        for _ in range(each_image_duration):
            video.write(image[1])

    cv2.destroyAllWindows()
    video.release()

    return video, video_name
