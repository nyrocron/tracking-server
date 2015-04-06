from django.contrib.auth.models import User
from django.core.management import BaseCommand
from tracker.models import TrackingSession




class Command(BaseCommand):
    args = '<session-id> <file>'
    help = 'Dump track from file'

    def handle(self, *args, **options):
        session_id, filename = args
        session = TrackingSession.objects.get(id=session_id)
        # user = models.ForeignKey(User)
        # start_time = models.DateTimeField()
        # end_time = models.DateTimeField(blank=True, null=True)
        # active = models.BooleanField(blank=True, default=True)
        # viewkey = models.CharField(max_length=32)
        # is_cleaned = models.BooleanField(blank=True, default=False)
        with open(filename, 'w') as out_file:
            out_file.re
