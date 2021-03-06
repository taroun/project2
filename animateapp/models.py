from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.


class Animate(models.Model):
    #맨처음 이미지 저장
    image = models.ImageField(upload_to='ani_image/', null=True)
    #만화책 방향이 좌->우 인지 우->좌 인지 확인
    left_right_choice = (('좌', '좌->우'), ('우', '우->좌'))
    left_right = models.CharField(max_length=5, choices=left_right_choice, default='좌')
    #분리되고 영상제작후 영상 파일 저장(mp4형식)
    ani = models.FileField(upload_to='ani/',
                           validators=[FileExtensionValidator(
                               allowed_extensions=['avi', 'mp4', 'mkv', 'mpeg', 'webm'])],
                           null=True,
                           blank=True)
    #생성일자
    created_at = models.DateField(auto_now_add=True, null=True)


