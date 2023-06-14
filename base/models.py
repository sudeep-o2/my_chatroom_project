from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True)
    about=models.TextField(null=True)

    avatar=models.ImageField(null=True,default='avatar.svg')

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]



class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated','-created']


    def __str__(self):
        return self.name


class Messages(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            self.body=self.body
        except:
            self.body='None'
        return self.body

    class Meta:
        ordering=['-updated','-created']


    @property
    def vmessage(self):
        try:
            message=self.body
        except:
            message=''
        return message

class MessageLikes(models.Model):

    liker=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    message=models.ForeignKey(Messages,on_delete=models.CASCADE,null=True,blank=True)
    
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.liker)


