from os import urandom
from json import loads, dumps

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone


class TrackingSession(models.Model):
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()
    active = models.BooleanField(default=True)
    viewkey = models.CharField(max_length=32)

    @staticmethod
    def create_session(user):
        for session in TrackingSession.objects.filter(user=user):
            session.finish()
        sess = TrackingSession(user=user, start_time=timezone.now(),
                               active=True, viewkey=random_string(16))
        sess.save()
        return sess

    def finish(self):
        self.active = False
        if self.trackedposition_set.count() > 0:
            self.save()
        else:
            self.delete()

    def as_json(self):
        points = [{
            'latitude': pos.latitude,
            'longitude': pos.longitude
        } for pos in self.trackedposition_set.all()]
        return dumps({
            'points': points,
            'active': self.active == True
        })


class TrackedPosition(models.Model):
    session = models.ForeignKey(TrackingSession)
    time = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    accuracy = models.FloatField()


class TrackingKey(models.Model):
    key = models.CharField(primary_key=True, max_length=32)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.key

    @staticmethod
    def create_key(user):
        """Create a new random key."""
        try:
            TrackingKey(user=user, key=random_string(16)).save()
        except IntegrityError:
            TrackingKey.create_key(user)


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
