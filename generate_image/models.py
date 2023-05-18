from django.db import models
from accounts.models import User

# Create your models here.
class GeneratedImage(models.Model):
    image = models.ImageField(upload_to='Images/generated_images')
    text_input = models.CharField(max_length=255,null=True)
    negative_prompt = models.CharField(max_length=255,null=True)
    style = models.CharField(max_length=100,null=True)
    number_of_images = models.IntegerField(null=True) 
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='generated_images')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_images')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    image = models.ForeignKey(GeneratedImage, on_delete=models.CASCADE, related_name='likes')



class UpscaledImage(models.Model):
    image = models.FileField(upload_to='upscaled_images/')
