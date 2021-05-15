from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out, login as log_in, authenticate
import pymongo
import json


from Mobooks.settings import DB_HOST


def index(request):
    return render(request, 'index.html', {})


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                log_in(request, user)
                return redirect('/')

    return render(request, 'register.html', {'form': form})


def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                log_in(request, user)
                return redirect('/')

    return render(request, 'login.html', {'form': form})


def logout(request):
    log_out(request)
    return redirect('/')


def connect_to_db():
    client = pymongo.MongoClient(DB_HOST, 27017)
    mobooks_db = client['mobooks']
    return mobooks_db


def populate_database(request):
    mobooks_db = connect_to_db()
    books_collection = mobooks_db['books']
    books_collection.drop()
    with open('static/pop_data/books.json') as file:
        data = json.load(file)
        books_collection.insert_many(data)

    authors_collection = mobooks_db['authors']
    authors_collection.drop()
    with open('static/pop_data/authors.json') as file:
        data = json.load(file)
        authors_collection.insert_many(data)

    genres_collection = mobooks_db['genres']
    genres_collection.drop()
    with open('static/pop_data/genres.json') as file:
        data = json.load(file)
        genres_collection.insert_many(data)

    publishers_collection = mobooks_db['publishers']
    publishers_collection.drop()
    with open('static/pop_data/publishers.json') as file:
        data = json.load(file)
        publishers_collection.insert_many(data)
        
    return render(request, 'index.html', {})