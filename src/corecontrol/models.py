# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class KnownUsers(models.Model):
    user_id = models.BigIntegerField(unique=True)
    screen_name = models.CharField(max_length=100)

    def __getitem__(self, key):
        return getattr(self, key)