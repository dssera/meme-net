from django.db import models
from django.contrib.auth.models import User
'''
title
body
pictureS 
likes
'''

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True)
    title = models.CharField(max_length=50,
                             blank=True)
    body = models.TextField(max_length=200, 
                            blank=True)
    likes = models.ManyToManyField(User, 
                                   related_name='post_like')
    
    def get_likes(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return self.author + ': ' + self.title
    

class Image(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    image = models.ImageField(upload_to='imgs')
    post = models.ForeignKey(to=Post, 
                             on_delete=models.CASCADE,
                             null=False)
    
    def __str__(self) -> str:
        return self.image.name


class Comment(TimeStampedModel):
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True)
    body = models.TextField(max_length=100)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self) -> str:
        return self.body[:20]

