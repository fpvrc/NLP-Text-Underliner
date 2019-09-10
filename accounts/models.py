from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Listings(models.Model):
    title = models.CharField(max_length=200)
    textracted = models.BooleanField(default=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, default='placeholder')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, default='placeholder')
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, default='placeholder')
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, default='placeholder')
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, default='placeholder')
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, default='placeholder')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Jreturns(models.Model):
    file_path = models.CharField(max_length=200)
    photo_id = models.IntegerField(null=True)
    user = models.IntegerField()
    def __str__(self):
        return self.photo_id

class Sum(models.Model):
    file_path = models.CharField(max_length=200)
    photo_id = models.IntegerField(null=True)
    user = models.IntegerField()
    def __str__(self):
        return self.photo_id


# class File(models.Model):
#     title = models.CharField(max_length=255, blank=True)
#     reading = models.ForeignKey(Listings, default=1, null=True, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='photos/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class File(models.Model):
    title = models.CharField(max_length=255, blank=True)
    reading = models.IntegerField(null=True)
    user = models.IntegerField(null=True)
    file = models.FileField(upload_to='photos/%Y/%m/%d/', blank=True, default='placeholder')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    textracted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('drag_and_drop_upload', kwargs={'id':self.id})

