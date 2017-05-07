from django.core.management.base import BaseCommand, CommandError

#from 
from calssync.utils import sync_calsusers


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        result = sync_calsusers()
