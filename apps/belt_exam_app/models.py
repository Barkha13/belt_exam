from __future__ import unicode_literals
import bcrypt
from django.db import models
# from datetime import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if (len(postData['name']) or len(postData['alias']) or len(postData['email']) or len(postData['pass']) or len(postData['conf_pass'])) < 1:
            errors['field_empty'] = "Fields can not be empty!"   
    
        if (len(postData['name']) or len(postData['alias'])) < 2:
            errors['name_length'] = "At least needs 2 characters for Name/Alias!!"
        
        if (not NAME_REGEX.match(postData['name'])) or (not NAME_REGEX.match(postData['alias'])):
            errors['name_type'] = "Name/Alias only contains letters!!"
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        
        if len(postData['pass']) < 8:
            errors['pass'] = "Password should be at least 8 characters long!"
        
        if postData['conf_pass'] != postData['pass']:
            errors['pass2'] = "Passwords didn't match!"
        return errors;

    def login_validator(self,postData):
        errors1 = {}
        if (len(postData['login_email']) or len(postData['login_pass'])) < 1:
            errors1['field_empty'] = "Fields can not be empty!"
        user_list = []
        user_list = User.objects.filter(email = postData['login_email'])
        if (user_list):
            login_pass = postData['login_pass']
            check = bcrypt.checkpw(login_pass.encode(),user_list[0].password.encode())
            if(check is False):
                errors1['wrong'] = "Wrong Username or Password!"
        else:
            errors1['wrong'] = "Wrong Username or Password!"
        return errors1;

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors2 = {}
        if len(postData['quoted_by']) < 3:
            errors2['quote'] = "At least needs 3 characters for Quoted By Field!!"
        if len(postData['message']) < 10:
            errors2['quote'] = "At least needs 10 characters for Message Field!!"
        return errors2;
            
            

            
class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    dob = models.DateField(auto_now = False, auto_now_add = False)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Quote(models.Model):
    quote = models.TextField()
    quoted_by = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name = "users_quotes")
    favorite = models.ManyToManyField(User, related_name = "favorite_quotes")
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = QuoteManager()

class Favorite(models.Model):
    quote = models.ForeignKey(Quote, related_name = "favorites")
    user = models.ForeignKey(User, related_name = "users_favorites")
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)





