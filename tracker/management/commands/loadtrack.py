from django.contrib.auth.models import User
from django.core.management import BaseCommand
from tracker.models import TrackingSession


class Command(BaseCommand):
    args = '<file> <username>'
    help = 'Load track from file'

    def handle(self, *args, **options):
        filename, username = args
        user = User.objects.get(username=username)
        session = TrackingSession.create_session(user)
        for line in filename:
            pass
