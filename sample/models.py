from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import os
# Create your models here.

class PathItem:
    name = ""
    parent = ""
    url = ""
    child = []
    canRead = True
    def __init__(self, name, parent,canRead1):
        self.name = name
        self.parent = parent
        self.url = os.path.join(parent, name)
        self.canRead = canRead1


class FileItem:
    name = ""
    parent = ""
    url = ""
    canRead = False

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.url = os.path.join(parent, name)


class Springport(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    port = models.IntegerField(auto_created=True,validators=[MinValueValidator(10000), MaxValueValidator(19999)])
    time = models.DateTimeField('生成日期', default=timezone.now)
    state = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Springports(models.Model):
    port = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time = models.DateTimeField('生成日期', default=timezone.now)
    state = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Mysqlports(models.Model):
    port = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time = models.DateTimeField('生成日期', default=timezone.now)
    state = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
"""
class Mysqlport(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    port = models.IntegerField(auto_created=True, validators=[MinValueValidator(20000), MaxValueValidator(29999)])
    date = models.DateTimeField('生成日期', default=timezone.now)
    state = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
"""
