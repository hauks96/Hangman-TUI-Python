from django.db import models
from .custom_errors import *
# Create your models here.
class Tablenames(models.Model):
    tname = models.CharField(primary_key=True, max_length=50, blank=False)
    byuser = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return self.tname

class Hangman(models.Model):
    word = models.CharField(max_length=60, blank=False)
    tablename = models.ForeignKey(Tablenames, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('word', 'tablename')
        
    def __str__(self):
        return self.word

class Users(models.Model):
    username = models.CharField(max_length=50, unique=True, blank=False)
    password = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return self.username

class History(models.Model):
    user = models.CharField(max_length=50, blank=False)
    score = models.IntegerField(default=0, blank=False)
    date = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return str(self.user)+" "+str(score)

class AuthorizationToken(models.Model):
    token = models.CharField(max_length=128, blank=False)
    date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(blank=False, default=True)
    user = models.CharField(max_length=50, blank=False)
