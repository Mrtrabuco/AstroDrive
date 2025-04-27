from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Cars(models.Model):
    year = models.SmallIntegerField(blank=True, null=True)
    make = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    model = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    trim = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    body = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    transmission = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    vin = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    state = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    condition = models.FloatField(blank=True, null=True)
    odometer = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    interior = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    seller = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    mmr = models.FloatField(blank=True, null=True)
    sellingprice = models.FloatField(blank=True, null=True)
    saledate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'

class Perfil(AbstractUser):
    foto = models.ImageField(
        upload_to='fotos_perfil/',
        null=True,
        blank=True,
        default='fotos_perfil/default.jpg'  # Imagen por defecto
    )

    def __str__(self):
        return f"Perfil de {self.username}"