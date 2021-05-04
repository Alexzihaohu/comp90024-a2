import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import json, requests, time, docker

import couchdb.couch as couch
import twitter_search.search_tweet as search
import twitter_stream.streamzihao as stream

class Command(BaseCommand):
    help = 'Initialise the databses required by this app'

    def handle(self, *args, **options): 
        stream.test()
        self.stdout.write(self.style.ERROR('Streaming stopped.'))
            