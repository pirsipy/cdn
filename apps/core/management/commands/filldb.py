import sys

from django.core.management.base import BaseCommand

from user.factories import AdminFactory


class Command(BaseCommand):
    help = 'Fill the database with test fixtures'

    def handle(self, *args, **options):
        sys.stdout.write('Starting fill db\r\n')

        AdminFactory()

        sys.stdout.write('Completed fill db\r\n')
