# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class KnownUsers(models.Model):
    user_id = models.BigIntegerField(unique=True)
    screen_name = models.CharField(max_length=100)

    def __getitem__(self, key):
        return getattr(self, key)


class InstanceTypes(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Instances(models.Model):
    name = models.CharField(max_length=50)
    ip = models.CharField(max_length=50)
    it = models.ForeignKey(InstanceTypes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name