from django.urls import include, path
from . import views
from django.contrib import admin

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),
    path('genre/<int:genre_id>', views.home, name='genre'),
    path('login', views.authentication, name= 'authentication_page'),
    path('createuser', views.signup, name='createuser'),
    path('loginuser', views.signin, name='loginuser'),
    path('logout_view', views.logout_view, name = 'logout_view'),
    path('addbook', views.postreview, name= 'addbook'),
    path('review', views.review_page, name= 'review_page'),
    path('book/<int:book_id>', views.book, name='book'),
    path('likebook/<int:book_id>', views.like, name='like'),
    path('searchbar', views.search, name= 'search'),
    path('logout', views.logout_view, name='logout'),
    path('homeauthentication', views.homeauthentication, name='homeauthentication'),
    path('author/<int:author_id>', views.author_view, name='author'),
]