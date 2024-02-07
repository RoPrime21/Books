from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book, Author, Genre, Review
from django.urls import reverse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



def signup(request):
    name = request.POST['name']
    lastname = request.POST['lastname']
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(first_name=name, email=email, last_name=lastname, username=username, password=password)
    user.save()
    login(request, user)
    print(name, lastname, username, password, email)

    return redirect('')


def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('books:home')
    else:
        print("Incorrect")
        return redirect('books:authentication_page')
    

def authentication(request):
   return render(request, 'books/authentication_page.html')


def logout_view(request):
    logout(request)

    return redirect('books:authentication_page')


def get_isbn(title, author_names):
    import requests
    url = 'https://www.googleapis.com/books/v1/volumes?q='

    url_title = title + ' ' + author_names
    
    url += url_title

    response = requests.get(url)
    data = response.json()

    try:
        first_book = data['items'][0]['volumeInfo']
        print(first_book)
        
        title = first_book['title']
        subtitle = first_book['subtitle']
        authors = first_book['authors']
        description = first_book['description']
        ids = first_book['industryIdentifiers']
        image = first_book['imageLinks']['thumbnail']
        image = image.replace('zoom=1', 'zoom=2')

        for identifier in ids:
            if identifier['type'] == 'ISBN_13':
                isbn = identifier['identifier']
                print(isbn)
                return {'title':title, 'subtitle':subtitle, 'authors':authors, 'isbn':isbn, 'description':description,
                        'image': image}
    except:
        return ''
    
    return ''

def postreview(request):
    print('Posting a review...')
    print(request.POST)
    book_name = request.POST['book_name']
    author_names = request.POST['authors_name']
    review = request.POST['review']
    genres = request.POST.getlist('genre')
    print(f'Genres selected: {genres}')

    ISBN_num = request.POST['ISBN']

    if not ISBN_num:
        book_info = get_isbn(book_name, author_names)
        print(book_info)
        
    if book_info:
        pass
        ##write your code here
    else:
        try:
            book = Book.objects.get(name=book_name)
            print(f'{book_name} already exists')
        except Book.DoesNotExist:
            book = Book(name=book_name)
            book.save()
            print(f'{book_name} saved in the database')

        authors = author_names.split(':')
        for author in authors:
            author = author.strip().title()

            try:
                a = Author.objects.get(name=author)
            except Author.DoesNotExist:
                a = Author(name=author)
                a.save()
        
            book.authors.add(a)
    
    for genre_id in genres:
        g = Genre.objects.get(id=genre_id)
        book.genres.add(g)


    # add this review of the book
    r = Review(book=book, review_text=review, reviewer=request.user)
    r.save()


    
    return redirect('books:home')

@login_required
def review_page(request):
    return render(request, 'books/post_page.html', context={'genres': Genre.objects.all()})

def book(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'books/book.html', context={'book': book})



def home(request, genre_id=None):
    genre = None
    if genre_id:
       genre = Genre.objects.get(id=genre_id)
       # todo: only pick books that belong to this genre
       books = Book.objects.filter(genres__id=genre_id)
    else:
       books = Book.objects.all()
    
    genres = Genre.objects.all()
    print(genres)

    context = {'books':books, 'genre': genre, 'genres': Genre.objects.all()}
   

    return render(request, 'books/home.html', context=context)    

def like(request, book_id):
    user = request.user
    book = Book.objects.get(id=book_id)

    if user in book.likers.all():
        book.likers.remove(user)
    else:
        book.likers.add(user)
        
    return redirect(request.META['HTTP_REFERER'])

def search(request):
    search_term = request.GET['searchbar']
    print(search_term)

    if not search_term:
        return redirect(request.META['HTTP_REFERER'])


    try:
        genres = Genre.objects.filter(genre__startswith = search_term)
        title_books = Book.objects.filter(name__startswith = search_term)
        author_books = Book.objects.filter(authors__in = Author.objects.filter(name__startswith=search_term))
        books = title_books.union(author_books)

    except Genre.DoesNotExist:
        pass


    context = {'genres': genres, 'search_term':search_term, 'books': title_books, 'authors':author_books}
    return render(request, 'books/search_results.html', context)

def logout_view(request):
    logout(request)
    return redirect('books:authentication_page')

def homeauthentication(request):
    return redirect('books:authentication_page')
    
def author_view(request, author_id):
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(authors__id=author_id)

    return render(request, "books/author.html", context={'author': author, 'books':books})

#For next week: wishlist, authors are clickable to page on what they wrote