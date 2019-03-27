# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime as dt
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True)
    profile_picture = models.ImageField(upload_to='profiles/')

    @classmethod
    def get_profiles(cls):
        '''
        Fucntion that gets all the profiles in the app
        Return
        '''
        profiles = Profile.objects.all()
        return profiles


class Image(models.Model):
    image = models.ImageField(upload_to='photos/', null=True)
    image_name = models.CharField(max_length=30)
    image_caption = models.TextField(max_length=100, null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['-date_uploaded']

    def save_image(self):
        '''Method to save an image in the database'''
        self.save()

    @classmethod
    def get_images(cls):
        '''
        Method that gets all image posts from the database
        Returns:
            images : list of image post objects from the database
        '''
        images = Image.objects.all()
        return images


class Follow(models.Model):
    user = models.ForeignKey(User)
    follower = models.ForeignKey(Profile, related_name='following')
    followee = models.ForeignKey(Profile, related_name='followers')

    def __str__(self):
        return self.user.username

    @classmethod
    def get_followees(cls, user_id):
        followeers = Follow.objects.filter(user=user_id).all()
        return followeers
