from django.db import models

class user(models.Model):
    name = models.CharField(max_length = 10)
    email = models.EmailField(unique = True)
    insta = models.CharField(max_length = 30,null=True,blank=True)