# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    items = models.ManyToManyField('Items')

    def __str__(self):
        return self.name


class Comments(models.Model):
    itemid = models.IntegerField(db_column='itemID', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Comments'


class Items(models.Model):
    itemid = models.AutoField(db_column='itemID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)  # This field type is a guess.
    path = models.TextField(blank=True, null=True)  # This field type is a guess.
    hash = models.TextField(blank=True, null=True)  # This field type is a guess.
    thumbnail = models.TextField(blank=True, null=True)  # This field type is a guess.
    found = models.IntegerField(blank=True, null=True) #legacy field, not needed
    date_added = models.DateTimeField(auto_now_add=True)  # Add the date_added field
   


    def __str__(self):
        return self.name

    def getTagNames(self):
        returnList = []
        for tag in Taggins.objects.filter(item=self):
            returnList.append(tag.tag)
        return returnList


    class Meta:
        managed = True
        db_table = 'Items'


class Release(models.Model):
    itemid = models.IntegerField(db_column='itemID', blank=True, null=True)  # Field name made lowercase.
    release = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Release'


class Taggins(models.Model):
    item = models.OneToOneField("Items",db_column="itemID", on_delete=models.CASCADE,default='')
    tag = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return self.tag

    class Meta:
        managed = False
        db_table = 'Taggins'
