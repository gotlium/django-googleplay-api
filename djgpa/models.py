# -*- coding: utf-8 -*-

import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from preferences.models import Preferences

from configs import TOKEN_FILE


class GooglePlayPreferences(Preferences):
    __module__ = 'preferences.models'

    android_id = models.CharField('Android ID', max_length=50)
    google_login = models.CharField('Google email', max_length=50)
    google_password = models.CharField('Google password', max_length=75)
    proxy_enabled = models.BooleanField('Use proxy', default=False)
    proxy_host = models.CharField(
        'Proxy host', max_length=50, blank=True, null=True)
    proxy_port = models.IntegerField(
        'Proxy port', max_length=5, blank=True, null=True)
    proxy_login = models.CharField(
        'Proxy login', max_length=50, blank=True, null=True)
    proxy_password = models.CharField(
        'Proxy password', max_length=75, blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = u'Google Play'
        verbose_name_plural = u'Google Play'


@receiver(post_save, sender=GooglePlayPreferences)
def remove_token(*args, **kwargs):
    if os.path.exists(TOKEN_FILE):
        os.unlink(TOKEN_FILE)
