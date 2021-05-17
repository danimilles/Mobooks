from django import forms

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
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control'}),
            'available_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
