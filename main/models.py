from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Género', unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=250, verbose_name='Autor')

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=150, verbose_name='Editorial')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=250, verbose_name='Título', null=False)
    release_year = models.IntegerField(verbose_name='Año de publicación', null=True)
    author = models.CharField(max_length=250, verbose_name='Autor', null=True)
    genre = models.CharField(max_length=250, verbose_name='Géneros', null=True)
    publisher = models.CharField(max_length=250, verbose_name='Editorial', null=True)
    synopsis = models.TextField(verbose_name='Sinopsis', null=False)
    available_quantity = models.IntegerField(verbose_name='Cantidad disponible', null=False)

    def __str__(self):
        return self.title
