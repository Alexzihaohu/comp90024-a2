"""
Jobs to run every minute. 
"""
import subprocess, time, random
from django.conf import settings
from django.core.cache import caches
from django_extensions.management.jobs import HourlyJob
from couchdb import couch


class Job(HourlyJob):
    help = "Spark Job"

    def execute(self):
        # This job only runs on 1 instance
        if settings.DJANGO_NODENAME.split('.')[1] != '1':
            return

        subprocess.Popen('spark-submit --master spark://spark:7077 --class endpoint /code/static/spark/user_rank.py', shell=True)