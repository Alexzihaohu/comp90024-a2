import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import json, requests, time, docker

import couchdb.couch as couch

class Command(BaseCommand):
    help = 'Initialise the views of each database'

    sports =  {'_id': '_design/sports',
 'views': {'wrestling': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'wrestling'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'weights': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'weights'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'skiing': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'skiing'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'water polo': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'water polo'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'volleyball': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'volleyball'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'tennis': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'tennis'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'team handball': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'team handball'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'table tennis': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'table tennis'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'swimming': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'swimming'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'surfing': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'surfing'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'sprinting': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'sprinting'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'skating': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'skating'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'soccer': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'soccer'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'skateboarding': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'skateboarding'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'shooting': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'shooting'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'rugby': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'rugby'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'rowing': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'rowing'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'rodeo': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'rodeo'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'racquetball': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'racquetball'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'squash': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'squash'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'pole vault': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'pole vault'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'running': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'running'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'martial arts': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'martial arts'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'jumps': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'jumps'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'lacrosse': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'lacrosse'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'ice hockey': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'ice hockey'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'jump': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'jump'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'gymnastics': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'gymnastics'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'golf': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'golf'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'football': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'football'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'fishing': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'fishing'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'field hockey': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'field hockey'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'fencing': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'fencing'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'equestrian': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'equestrian'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'diving': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'diving'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'cycling': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'cycling'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'curling': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'curling'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'cheerleading': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'cheerleading'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'canoe': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'canoe'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'kayak': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'kayak'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'bull': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'bull'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'bareback': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'bareback'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'bronc riding': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'bronc riding'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'boxing': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'boxing'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'bowling': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'bowling'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'bobsledding': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'bobsledding'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'luge': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'luge'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'billiards': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'billiards'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'basketball': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'basketball'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'baseball': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'baseball'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'softball': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'softball'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'badminton': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'badminton'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'racing': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'racing'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",},
  'archery': {'reduce': '_count',
   'map': "function (doc) {\n  sport = 'archery'\n  if (doc.val.text.toLowerCase().includes(sport))\n   {emit(doc._id, 1); }\n}",}},
 'language': 'javascript',
 'options': {'partitioned': True}}

couch.put('twitters/_design/sports', body=sports)