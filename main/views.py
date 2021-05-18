from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out, login as log_in, authenticate
import pymongo
import json

from Mobooks.settings import DB_HOST
from main.forms import SearchForm, BookForm
from main.models import Book, Author, Genre, Publisher


# Index
def index(request):
    return render(request, 'index.html', {})


# Login
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                log_in(request, user)
                return redirect('/')

    return render(request, 'form.html', {'form': form, 'title': 'Registro'})


def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                log_in(request, user)
                return redirect('/')

    return render(request, 'form.html', {'form': form, 'title': 'Iniciar sesión'})


def logout(request):
    log_out(request)
    return redirect('/')


# Population
def connect_to_db():
    client = pymongo.MongoClient(DB_HOST, 27017)
    mobooks_db = client['mobooks']
    return mobooks_db


def populate_database(request):
    mobooks_db = connect_to_db()

    books_collection = mobooks_db['main_book']
    books_collection.drop()
    with open('static/pop_data/books.json') as file:
        data = json.load(file)
        for datum in data:
            book = Book(title=datum['title'],
                        release_year=datum['release_year'],
                        author=datum['author'],
                        genre=datum['genre'],
                        publisher=datum['publisher'],
                        synopsis=datum['synopsis'],
                        available_quantity=datum['available_quantity'])
            Book.save(book)

    authors_collection = mobooks_db['main_author']
    authors_collection.drop()
    with open('static/pop_data/authors.json') as file:
        data = json.load(file)
        for datum in data:
            author = Author(name=datum['author'])
            Author.save(author)

    genres_collection = mobooks_db['main_genre']
    genres_collection.drop()
    with open('static/pop_data/genres.json') as file:
        data = json.load(file)
        for datum in data:
            genre = Genre(name=datum['genre'])
            Genre.save(genre)

    publishers_collection = mobooks_db['main_publisher']
    publishers_collection.drop()
    with open('static/pop_data/publishers.json') as file:
        data = json.load(file)
        for datum in data:
            publisher = Publisher(name=datum['publisher'])
            Publisher.save(publisher)
    return redirect('/')


# Search
def search(request):
    form = SearchForm()
    mobooks_db = connect_to_db()

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            page = form.cleaned_data.get('page')
            to_show = form.cleaned_data.get('to_show')
            to_skip = (page - 1) * to_show

            order_type = form.cleaned_data.get('order_type')
            reverse = form.cleaned_data.get('reverse')
            asc_or_desc = 1 if reverse is False else -1

            query = {}
            title = form.cleaned_data.get('title')
            match = form.cleaned_data.get('match')
            if title:
                query['title'] = {"$regex": "(.*)" + title + "(.*)"} if not match else title

            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')
            if from_date or to_date:
                date_compare = {}
                if from_date:
                    date_compare["$gte"] = from_date
                if to_date:
                    date_compare["$lte"] = to_date

                query['release_year'] = date_compare

            genre = form.cleaned_data.get('genre')
            if genre:
                query['genre'] = str(genre)

            publisher = form.cleaned_data.get('publisher')
            if publisher:
                query['publisher'] = str(publisher)

            author = form.cleaned_data.get('author')
            if author:
                query['author'] = str(author)

            books = mobooks_db.main_book.find(query).sort(order_type, asc_or_desc).skip(to_skip).limit(to_show)
            return render(request, 'search.html',
                          {'form': form, 'books': books})

    return render(request, 'search.html',
                  {'form': form, 'books': mobooks_db.main_book.find().sort("title", 1).limit(10)})

# Statistics
def statistics(request):
    mobooks_db = connect_to_db()

    available_books_num = 0
    for book in mobooks_db.main_book.find():
        available_books_num += book["available_quantity"]

    return render(request, 'statistics.html',
                  {'statistics':
                       {"books_num": mobooks_db.main_book.find().count(),
                        "genres_num": mobooks_db.main_genre.find().count(),
                        "authors_num": mobooks_db.main_author.find().count(),
                        "publishers_num": mobooks_db.main_publisher.find().count(),
                        "available_books_num": available_books_num}
                   })


# CRUD
def details(request, id_book):
    mobooks_db = connect_to_db()
    return render(request, 'details.html', {'book': mobooks_db.main_book.find({"id": id_book}).next()})


def create(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(data=request.POST)

        if form.is_valid():
            book = Book.objects.create(title=form.cleaned_data['title'],
                                       release_year=form.cleaned_data['release_year'],
                                       author=form.cleaned_data['author'],
                                       genre=form.cleaned_data['genre'],
                                       publisher=form.cleaned_data['publisher'],
                                       synopsis=form.cleaned_data['synopsis'],
                                       available_quantity=form.cleaned_data['available_quantity'])
            check_create_integrity(book)
            return redirect('/book/' + str(book.id))

    return render(request, 'form.html', {'form': form, 'title': 'Crear libro'})


def edit(request, id_book):
    book = Book.objects.get(pk=id_book)
    book_copy = Book(title=book.title,
                     release_year=book.release_year,
                     author=book.author,
                     genre=book.genre,
                     publisher=book.publisher,
                     synopsis=book.synopsis,
                     available_quantity=book.available_quantity)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(data=request.POST, instance=book)

        if form.is_valid():
            form.save()
            check_delete_integrity(book_copy)
            check_create_integrity(book)
            return redirect('/book/' + str(book.id))

    return render(request, 'form.html', {'form': form, 'title': 'Editar libro'})


def delete(request, id_book):
    book = Book.objects.get(pk=id_book)
    book.delete()
    check_delete_integrity(book)
    return redirect('/book/search')


def check_delete_integrity(initial_book):
    mobooks_db = connect_to_db()
    if mobooks_db.main_book.find({'author': initial_book.author}).count() == 0:
        mobooks_db.main_author.remove({'name': initial_book.author})
    if mobooks_db.main_book.find({'genre': initial_book.genre}).count() == 0:
        mobooks_db.main_genre.remove({'name': initial_book.genre})
    if mobooks_db.main_book.find({'publisher': initial_book.publisher}).count() == 0:
        mobooks_db.main_publisher.remove({'name': initial_book.publisher})


def check_create_integrity(initial_book):
    mobooks_db = connect_to_db()
    if mobooks_db.main_author.find({'name': initial_book.author}).count() == 0:
        Author.objects.create(name=initial_book.author)
    if mobooks_db.main_genre.find({'name': initial_book.genre}).count() == 0:
        Genre.objects.create(name=initial_book.genre)
    if mobooks_db.main_publisher.find({'name': initial_book.publisher}).count() == 0:
        Publisher.objects.create(name=initial_book.publisher)
