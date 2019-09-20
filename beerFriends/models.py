from datetime import datetime

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

image_storage = FileSystemStorage(
    location=u'{0}/images/'.format(settings.MEDIA_ROOT),
    base_url=u'{0}'.format(settings.MEDIA_URL),
)


def image_directory_path(instance, filename):
    return u'{0}'.format(filename)


class Beer(models.Model):
    name = models.CharField(max_length=250, null=True)
    addedOn = models.DateField(default=datetime.now, blank=True)
    origin = models.CharField(max_length=250, null=True)
    rating = models.FloatField(null=True, blank=True)
    image = CloudinaryField('image', null=True)
    alcoholContent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], max_length=10, null=True, blank=True)


class Review(models.Model):
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True)
    text = models.CharField(max_length=250, null=True)
    creator = models.CharField(max_length=250, null=True)
