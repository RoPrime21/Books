from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.genre
    
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    description = models.TextField(blank=True)
    image_link = models.URLField(blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=30, blank=True)
    likers = models.ManyToManyField(User, related_name='book_likers')
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
    
    def __str__(self) -> str:
        return self.name

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    reviewer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reviewer')
    

