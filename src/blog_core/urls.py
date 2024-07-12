from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [ 
    path('posts/', views.index, name='memes'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/delete/', views.delete_post, name='delete_post'),
    path('posts/change/', views.change_post, name='change_post'),


]
