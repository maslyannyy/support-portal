from django.core.management.base import BaseCommand

from tasks.services.feeds import check_feeds


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_feeds()
