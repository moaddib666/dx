import requests
from django.core.management.base import BaseCommand
from apps.adapters.centrifugo.client import CentrifugoClient

class Command(BaseCommand):
    help = 'Broadcast a message to multiple Centrifugo channels'

    def add_arguments(self, parser):
        parser.add_argument('channels', type=str, nargs='+', help='The channels to send the message to')
        parser.add_argument('message', type=str, help='The message to send')

    def handle(self, *args, **kwargs):
        channels = kwargs['channels']
        message = kwargs['message']

        client = CentrifugoClient()
        try:
            response = client.broadcast(channels, {"message": message})
            self.stdout.write(self.style.SUCCESS(f'Successfully broadcasted message to {", ".join(channels)}'))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to broadcast message to channels: {e}'))
