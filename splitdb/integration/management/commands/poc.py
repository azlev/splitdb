from django.core.management.base import BaseCommand, CommandError
from django.db.models.query import Prefetch

from loggi.models import Father
from integration.models import Son

class Command(BaseCommand):
    help = 'Proof of Concept of prefetch from a different database'

    def handle(self, *args, **options):
        qs = Father.objects.using('default').all()
        pf = Prefetch('father', qs)

        s1 = Son.objects.all()
        s2 = s1.prefetch_related(pf).order_by('id')

        for s in s2:
            self.stdout.write(f"Son: {s}, Father: {s.father}")

