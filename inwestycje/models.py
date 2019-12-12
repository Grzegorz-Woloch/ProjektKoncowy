from django.db import models
from django.contrib.auth.models import User




# nazwa produktu i opis krotki
class Product(models.Model):
    name = models.CharField(max_length=164)
    description = models.TextField()
    profitability = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    files = models.FileField(upload_to='media/', default='settings.MEDIA_ROOT/media/random_photo.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Kategoria produktu
class Category(models.Model):
    name = models.CharField(max_length=164)
    product = models.ManyToManyField(Product)
