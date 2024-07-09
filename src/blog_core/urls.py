from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [ 
    path('posts/', views.index, name='memes'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail')
]
