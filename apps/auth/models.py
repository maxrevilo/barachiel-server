#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
from django.db import models


class Confirmation(models.Model):

    VALID_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits
    EMAIL = 'E'
    PHONE = 'P'
    TYPE_CHOICES = ((EMAIL, 'E-Mail'), (PHONE, 'Phone Number'))

    user = models.ForeignKey('users.User', related_name='confirmations', on_delete=models.CASCADE)
    token = models.CharField(max_length=8, unique=True)
    confirmation_type = models.CharField(choices=TYPE_CHOICES, max_length=1)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
