import datetime

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from animateapp.forms import AnimateCreationForm
from animateapp.models import Animate

from PIL import Image
import pytesseract
import cv2.cv2 as cv2
import os

#pytesseract 환경변수 지정후 위치 받아오는부분
#설정 해줘야 작동이 됨
pytesseract.pytesseract.tesseract_cmd = R'C:\Django\lib\Tesseract-OCR\tesseract'


class AnimateCreateView(CreateView):
    model = Animate
    form_class = AnimateCreationForm
    template_name = 'animateapp/create.html'

    def form_valid(self, form):
        #form 저장
        temp_upload = form.save(commit=False)
        temp_upload.save()
        temp_upload = form.save(commit=False)
        #이미지 저장된 위치 가져오기
        path = 'media/' + str(temp_upload.image)
        #좌우 만화책 방향 가져오기
        l_r = str(temp_upload.left_right)

        #crop(이미지 저장위치, 만화책방향)-임시로 이미지를 분할해서 글자수까지 나타내는함수
        #반환값은 cut의 [순서,이미지,글자수]의 리스트
        image_len_list = crop(path, l_r)

        #view_seconds(image_len_list)-cut의 순서 이미지 글자수를 가지고 영상화하는 함수
        #반환값은 영상 저장 위치
        video_path = view_seconds(image_len_list)

        #영상까지 form 저장
        temp_upload.ani = video_path
        temp_upload.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('animateapp:detail', kwargs={'pk': self.object.pk})


class AnimateDetailView(DetailView):
    model = Animate
    context_object_name = 'target_animate'
    template_name = 'animateapp/detail.html'


#임시로 이미지 분할
#앞으로 컷분리 모델이 들어갈 부분
def crop(path, l_r):
    #이미지 저장위치로 이미지 받아옮
    im = Image.open(path)
    #이미지 width, height 값 받아옮
    img_width, img_height = im.size

    #opencv 이미지 읽어오기
    src = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    #이미지 3등분하기위한 높이값 나눔
    hei_3 = int(img_height / 3)
    #잘려진 cut과 순서 글자수를 넣을 리스트 미리생성
    crop_img = []
    # 이미지를 자른다.
    for i in range(3):
        #이미지를 [높이 나누는 부분: 넓이 전체]로 복사함
        dst = src[hei_3*i:hei_3*(i+1):, 0:img_width].copy()
        #img_text_len(dst)-잘려진cut으로 이미지로 글자수 측정 함수
        #반환값은 cut의 글자수
        txt_len = img_text_len(dst)
        #리스트에 순서, cut image, 글자수 추가
        crop_img.append([i, dst, txt_len])
    #cut의 [순서,이미지,글자수]의 리스트 반환
    return crop_img


#img_text_len(img)-이미지를 받아 글자수를 반환해주는 함수
def img_text_len(img):
    #pytesseract.image_to_string(이미지, 언어, 옵션)-tesseract의 ocr-이미지의 글자를 text형태로 반환
    out_text = pytesseract.image_to_string(img, lang='kor+eng', config='--psm 1 -c preserve_interword_spaces=1')
    #반환된 text의 줄바꿈과 앞,뒤 공백등을 제거
    out_text = out_text.replace("\n", "")
    out_text.strip()
    print("길이:" + str(len(out_text)))
    print(out_text)
    #글자수를 반환
    return len(out_text)


#[순서,이미지,글자수]의 리스트를 받아 영상으로 만들고 저장하는 함수
def view_seconds(image_list):
    #영상이름 오늘 날자와 시간으로 지정
    nowdate = datetime.datetime.now()
    daytime = nowdate.strftime("%Y-%m-%d_%H%M%S")
    #영상 저장 위치 설정
    video_name = 'ani/' + daytime + '.mp4'
    out_path = 'media/' + video_name
    #video codec 설정
    fourcc = cv2.VideoWriter_fourcc(*'H264')

    #현재 영상 프레임을 첫번째이미지로 설정(변경가능)
    frame = image_list[0][1]
    height, width, layers = frame.shape

    #video작성부분(저장위치, codec, fps, 영상프레임)
    video = cv2.VideoWriter(out_path, fourcc, 1.0, (width, height))
    #리스트에서 한 cut씩 가져옮
    for image in image_list:
        #기본 5초에 이미지의 글자수를 10으로 나눈만큼 반복하여 같은 이미지 기록
        each_image_duration = 5 + int(image[2]/10)
        for _ in range(each_image_duration):
            video.write(image[1])

    #객체를 반드시 종료시켜주어야 한다
    video.release()
    #모든 화면 종료해준다.
    cv2.destroyAllWindows()

    #영상 저장 위치 반환
    return video_name
