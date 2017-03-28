from __future__ import unicode_literals

from django.db import models

import re
import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        dateNow = datetime.datetime.today().strftime('%Y-%m-%d')
        errors = []
        if len(postData['name']) < 3:
            errors.append('Name must be at least 3 letters')
        if postData['name'].isdigit():
            errors.append('Name cannot contain numbers')
        if len(postData['username']) < 3:
            errors.append('Username must be at least 3 characters')
        if len(postData['password']) < 8:
            errors.append('Password too short')
        if postData['password'] != postData['confirmpw']:
            errors.append('Passwords do not match')
        if not errors:
            password = postData['password'].encode()
            password = bcrypt.hashpw(password, bcrypt.gensalt())
            if self.filter(username=postData['username']).exists():
                errors.append('Username is already registered')
                return { 'error': errors }
            else:
                user = self.create(name = postData['name'], username = postData['username'], password = password)
                return { "theuser": user }
        else:
            return { "error": errors }

    def login(self, postData):
        errors = []
        if self.filter(username = postData['username']).exists():
            password = postData['password'].encode('utf-8')
            stored_hash = User.objects.get(username=postData['username']).password
            if bcrypt.hashpw(password, stored_hash.encode('utf-8')) != stored_hash:
                errors.append('incorrect password')
            else:
                user = self.get(username = postData['username'])
        else:
            errors.append('Username does not exist')
        if not errors:
            return { "theuser": user }
        else:
            return { "error": errors }

class TripManager(models.Manager):
    def add(self, postData):
        errors = []
        dateNow = datetime.datetime.today().strftime('%Y-%m-%d')
        if not len(postData['destination']) > 0:
            errors.append('Please enter a destination')
        if not len(postData['description']) > 0:
            errors.append('Please enter a description')
        if postData['startdate'] < dateNow:
            errors.append('Invalid travel start date')
        if postData['enddate'] < postData['startdate']:
            errors.append('Travel end date cannot be before start date')
        if not errors:
            user = User.objects.get(id = postData['user_id'])
            trip = self.create(destination = postData['destination'], description = postData['description'], user = user, startdate = postData['startdate'], enddate = postData['enddate'])
            return { 'trip': trip }
        else:
            return { 'error': errors }

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    startdate = models.DateField()
    enddate = models.DateField()
    objects = TripManager()
    user = models.ForeignKey(User)
    attendees = models.ManyToManyField(User, related_name="attendees")
