from os import urandom
from json import loads, dumps

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone

from gpxpy import gpx


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

    def title(self):
        return self.start_time.strftime('%Y-%m-%d_%H-%M-%S')

    def finish(self):
        self.active = False
        if self.trackedposition_set.count() > 0:
            self.save()
        else:
            self.delete()

    def as_json(self, from_id=None):
        if from_id is None:
            positions = self.trackedposition_set.all()
        else:
            positions = self.trackedposition_set.filter(id__gt=from_id)

        points = [{
            'latitude': pos.latitude,
            'longitude': pos.longitude,
            'id': pos.id
        } for pos in positions]
        return dumps({
            'points': points,
            'active': self.active
        })

    def as_gpx(self):
        segment = gpx.GPXTrackSegment()
        for pos in self.trackedposition_set.all():
            track_point = gpx.GPXTrackPoint(pos.latitude, pos.longitude, pos.altitude)
            segment.points.append(track_point)
        track = gpx.GPXTrack()
        track.segments.append(segment)
        gpx_obj = gpx.GPX()
        gpx_obj.tracks.append(track)
        return gpx_obj.to_xml()


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
