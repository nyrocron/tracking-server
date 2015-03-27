from django.db import models
from django.contrib.auth.models import User

from os import urandom

class TrackedPosition(models.Model):
    time = models.DateTimeField()
    user = models.ForeignKey(User)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    accuracy = models.FloatField()

class TrackingKey(models.Model):
    user = models.ForeignKey(User, primary_key=True)
    key = models.CharField()

    VALID_CHARACTERS = "abcdefghijklmnopqrstuvwxyz"

    @staticmethod
    def create_key(user):
        k = TrackingKey(user=user, key=TrackingKey._random_string(16))
        k.save()

    @staticmethod
    def _random_string(n):
        str_parts = []
        str_len = 0
        while str_len < n:
            random_bytes = urandom(20 * n)
            filtered = ''.join([chr(x) for x in random_bytes if 97 <= x <= 122])
            str_parts.append(filtered)
            str_len += len(filtered)
        return ''.join(str_parts)[:n]

class ViewKey(models.Model):
    pass
