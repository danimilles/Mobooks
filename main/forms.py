from django import forms
from django.forms import Textarea

from main.models import Genre, Book


class OrderField(forms.Form):
    choices = (
        ('title', 'Título'), ('available_quantity', 'Cantidad'), ('release_date', 'Fecha de publicación'))
    order_type = forms.ChoiceField(choices=choices, required=False, label='Ordenar por')
    reverse = forms.BooleanField(required=False, label='Al revés')
    page = forms.IntegerField(required=True, label='Página', min_value=1, initial=1)


class SearchForm(OrderField):
    genre = forms.ModelChoiceField(queryset=Genre.objects.all().order_by('name'), label='Género')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'release_year', 'author', 'genre', 'publisher', 'synopsis', 'available_quantity']
    title = forms.CharField(max_length=250, label='Título*', required=True)
    release_year = forms.IntegerField(label='Año de publicación (Negativo para a. C.)', max_value=2021, required=False, initial=2020)
    author = forms.CharField(max_length=250, label='Autor', required=False)
    genre = forms.CharField(max_length=250, label='Género', required=False)
    publisher = forms.CharField(max_length=250, label='Editorial', required=False)
    synopsis = forms.CharField(max_length=2500, label='Sinopsis*', required=True, widget=Textarea)
    available_quantity = forms.IntegerField(label='Cantidad disponible*', required=True, min_value=0, initial=0)

