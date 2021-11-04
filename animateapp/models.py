from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.


class Animate(models.Model):
    image = models.ImageField(upload_to='ani_image/', null=True)
    ani = models.FileField(upload_to='ani/',
                           validators=[FileExtensionValidator(allowed_extensions=['avi', 'mp4', 'mkv', 'mpeg', 'webm'])],
                           null=True,
                           blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)


