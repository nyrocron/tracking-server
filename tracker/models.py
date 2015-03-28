from os import urandom
from json import loads, dumps

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone


class TrackingSession(models.Model):
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()

    @staticmethod
    def create_session(user):
        sess = TrackingSession(user=user, start_time=timezone.now())
        sess.save()
        return sess

    def add_position(self, position_dict):
        """Add a new TrackedPosition with the given data"""
        raise NotImplementedError()

    def as_json(self):
        points = [{
            'latitude': pos.latitude,
            'longitude': pos.longitude
        } for pos in self.trackedposition_set.all()]
        return dumps({
            'points': points
        })


class TrackedPosition(models.Model):
    session = models.ForeignKey(TrackingSession)
    time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    accuracy = models.FloatField()

    @staticmethod
    def from_json(session, json_string):
        json_dict = loads(json_string)
        tp = TrackedPosition(**json_dict)
        tp.session = session
        tp.save()
        return tp


class TrackingKey(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.key

    @staticmethod
    def create_key(user):
        """Create a new random key."""
        if user.trackingkey:
            user.trackingkey.delete()
        TrackingKey(user=user, key=random_string(16)).save()


class ViewKey(models.Model):
    sessions = models.ManyToManyField(TrackingSession, blank=True)
    key = models.CharField(primary_key=True, max_length=32)

    def __str__(self):
        return self.key

    @staticmethod
    def create_key():
        """Create a new random key."""
        k = ViewKey(key=random_string(16))
        try:
            k.save()
        except IntegrityError:
            return ViewKey.create_key()
        return k


def random_string(n):
    """Create a random string of length n.

    Uses os.urandom for relatively secure random values.
    """
    str_parts = []
    str_len = 0
    while str_len < n:
        random_bytes = urandom(20 * n)
        filtered = ''.join([chr(x) for x in random_bytes if 97 <= x <= 122])
        str_parts.append(filtered)
        str_len += len(filtered)
    return ''.join(str_parts)[:n]
