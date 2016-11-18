from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=90)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)

class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=90)

class Reviews(models.Model):
    user_id = models.ForeignKey(Users)
    book_id = models.ForeignKey(Books)
    rating = models.IntegerField()
    review = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
