from django.db import models

# Create your models here.


class CropAni(models.Model):
    image = models.ImageField(upload_to='animate/', null=True)
    created_at = models.DateField(auto_now_add=True, null=True)


class CutTime(models.Model):
    image = models.ForeignKey(CropAni, on_delete=models.CASCADE, related_name='animate')
    cut = models.ImageField(upload_to='article/crop/', null=True)
    length = models.CharField(max_length=25, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

