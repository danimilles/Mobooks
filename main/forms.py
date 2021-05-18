from django import forms

from main.models import Genre, Book, Publisher, Author


class OrderField(forms.Form):
    choices = (
        ('title', 'Título'), ('release_year', 'Año de publicación'))
    order_type = forms.ChoiceField(choices=choices, required=False, label='Ordenar por')
    reverse = forms.BooleanField(required=False, label='Al revés')
    page = forms.IntegerField(required=True, label='Página', min_value=1, initial=1)
    to_show = forms.IntegerField(required=True, label='Número de libros para mostrar', min_value=1, initial=10)


class SearchForm(OrderField):
    title = forms.CharField(max_length=250, label='Título', required=False)
    match = forms.BooleanField(label='Coincidir totalmente', required=False)
    from_date = forms.IntegerField(label='Desde año de publicación', required=False)
    to_date = forms.IntegerField(label='Hasta año de publicación', required=False)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all().exclude(name=None).order_by('name'), label='Género',
                                   required=False)
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all().exclude(name=None).order_by('name'),
                                       label='Editorial', required=False)
    author = forms.ModelChoiceField(queryset=Author.objects.all().exclude(name=None).order_by('name'), label='Autor',
                                    required=False)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'release_year', 'author', 'genre', 'publisher', 'synopsis', 'available_quantity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
