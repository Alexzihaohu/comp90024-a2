from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import HttpResponse
from django.conf import settings 
from collections import Counter
import json, time, os
import couchdb.couch as couch

# https://www.django-rest-framework.org/api-guide/viewsets/
# https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.QueryDict.urlencode
class TweetViewSet(viewsets.ViewSet):

    # GET analyser/tweets?options 
    # Add include_docs=true
    def list(self, request):
        url = f'tweetdb/_all_docs'
        if len(request.query_params) > 0: 
            url += f'?{request.query_params.urlencode()}'
        res = couch.get(url)
        return Response(res.json())

    # GET analyser/tweets/:id
    def retrieve(self, request, pk=None):
        res = couch.get(f'tweetdb/{pk}')
        return Response(couch.get('twitter', pk).json())

    # GET analyser/tweets/stats/
    @action(detail=False, methods=['get'], name="Get the stats of tweets")
    def stats(self, request):
        count = {}
        for city in ["Melbourne", "Sydney", "Canberra", "Adelaide"]:
            res = couch.get(f'tweetdb/_partition/{city}')
            count[city] = res.json()["doc_count"]
        count["total_tweets"] = sum(count.values())
        return HttpResponse(json.dumps({"tweet_stats": count}))
    
    # GET analyser/tweets/sports/ sport related tweets
    @action(detail=False, methods=['get'], name="sport tweets total")
    def sports(self, request):
        # count = 0
        res1 = {}
        for city in ["Melbourne", "Sydney", "Canberra", "Adelaide"]:
            # res = couch.get(f'tweetdb/_partition/{city}/_design/filter/_view/new-view')
            res = couch.get(f'tweetdb/_partition/{city}/_design/sports/_view/total')
            res1[city]=res.json()['rows'][0]["value"]
            # count += res.json()['rows'][0]["value"]
        return HttpResponse(json.dumps(res1))
    
class UserViewSet(viewsets.ViewSet):

    # GET analyser/users/
    def list(self, request):
        actions = {
            'stats': 'Stats of users.',
            'rank': 'Get the sporst enthusiasts rank'
        }
        return Response(actions)

    # GET analyser/users/stats
    @action(detail=False, methods=['get'], name="Get the stats of users")
    def stats(self, request):
        count = {}
        for city in ["mel", "syd", "cbr", "adl"]:
            res = couch.get(f'userdb/_design/cities/_view/{city}')
            # count[city] = res.json()["doc_count"]
            count[city] = res.json()['rows'][0]["value"]
        count["total_users"] = sum(count.values())
        return Response({"user_stats": count})

    # GET analyser/users/rank
    @action(detail=False, methods=['get'], name="Get the rank of the enthusiasts")
    def rank(self, request):
        res = couch.get('conclusions/user_rank')
        return Response(res.json())
class SportViewSet(viewsets.ViewSet):

    # GET analyser/sports/
    def list(self, request):
        actions = {
            'stats_all': 'All sport counts in all cities cross all time.',
            ':year': 'All sport counts in all cities cross in the year number'
        }
        return Response(actions)

    # GET analyser/sports/stats_all
    @action(detail=False, methods=['get'], name="Get the static_stats of sports")
    def stats_all(self, request):
        count = {}
        sum_all = {}
        for city in ["Melbourne", "Sydney", "Canberra", "Adelaide"]:
            res = couch.get(f'tweetdb/_partition/{city}/_design/sports/_view/total')
            res = Counter(res.json()['rows'][0]["value"])
            sum_all[city] = sum(res.values())
            count[city] = res
        total = Counter() # all sports
        for k in count.keys():
            total += count[k]
        count['total'] = total
        sum_all['total'] = sum(sum_all.values())
        count['sum'] = sum_all
        return HttpResponse(json.dumps(count))

    # GET analyser/sports/rank_top3
    @action(detail=False, methods=['get'], name="Get the top 3 sports in each city across all time")
    def rank_top3(self, request):
        count = {}
        for city in ["Melbourne", "Sydney", "Canberra", "Adelaide"]:
            res = couch.get(f'tweetdb/_partition/{city}/_design/sports/_view/total')
            res = Counter(res.json()['rows'][0]["value"])
            top3 = {}
            for i in res.most_common(3):
                top3[i[0]] = i[1]
            count[city] = top3
        return HttpResponse(json.dumps(count))

    # GET analyser/sports/yearly_stats
    @action(detail=False, methods=['get'], name="Get the 2019, 2020, 2021 tweets of sports in each city")
    def yearly_stats(self, request):
        count = {}
        for city in ["Melbourne", "Sydney", "Canberra", "Adelaide"]:
            time_line = {}
            for time_stamp in ['2019', '2020', '2021']:
                res = couch.get(f'tweetdb/_partition/{city}/_design/sports/_view/{time_stamp}')
                res = Counter(res.json()['rows'][0]["value"])
                time_line[time_stamp] = sum(res.values())
            count[city] = time_line
        return HttpResponse(json.dumps(count))

    # GET analyser/sports/:year Get the year tweets of sports
    def retrieve(self, request, pk=None):
        count = {}

        if pk is None or not isinstance(pk, int):
            return Response(0)
        else: 
            pk = int(pk)

        for city in ["Melbourne", "Sydney", "Canberra", "Adelaide"]:
            res = couch.get(f'tweetdb/_partition/{city}/_design/sports/_view/{pk}')

            if res.json()['rows']:
                res = Counter(res.json()['rows'][0]["value"])
            else:
                res = Counter()
            count[city] = res
        total = Counter() # all sports
        for k in count.keys():
            total += count[k]
        count['total'] = total
        return Response(count)

class AurinViewSet(viewsets.ViewSet):
    # GET /aurin/
    def list(self, request):
        res = couch.get(f'aurin/_design/cities/_view/aurinInfo')
        return Response(res.json())

# Jobs statuses in Couchdb. Background tasks will periodically check the statuses to  
# start the jobs. 
class JobsViewSet(viewsets.ViewSet):
    # GET /analyser/jobs/
    def list(self, request):
        return Response(couch.get(f'jobs/_all_docs').json())

    # GET /analyser/jobs/search/
    # GET /analyser/jobs/update/
    # GET /analyser/jobs/stream/
    # GET /analyser/jobs/user_rank/
    # GET /analyser/jobs/couchdb/
    def retrieve(self, request, pk=None):
        if pk is None: 
            return Response({'error': 'job name is missing'})
        return Response(couch.get(f'jobs/{pk}').json())

    # PUT /analyser/jobs/search/ -d {"new_users": 1000}
    # PUT /analyser/jobs/update/
    # PUT /analyser/jobs/stream/
    # PUT /analyser/jobs/user_rank/
    # PUT /analyser/jobs/couchdb/
    def update(self, request, pk=None):
        try: 
            # get new users and timelines
            if pk == 'search': 
                return self.start_search(request)
            
            # update existing user timelines
            elif pk == 'update':
                return self.start_update()
            
            # start streaming
            elif pk == 'stream':
                return self.start_stream()
            
            # start calculating users rank
            elif pk == 'stream':
                return self.calculate_user_rank()
            
            # migrate couchdb 
            elif pk == 'couchdb':
                return self.migrate_couchdb()

            else: 
                return Response({'error': f'Invalid job name {pk}'}) 
        except Exception as e: 
            return Response(str(e)) 

    def start_search(self, request): 
        new_users = request.data.get('new_users') if request.data is not None else None
        if isinstance(new_users, int): 
            new_users = int(new_users)
        else: 
            return Response({'error': 'Parameter new_users is not provided'}, 403)

        res = couch.get('jobs/search')
        if res.status_code == 200 and res.json().get('status') != 'done':
            return Response(res.json(), 403)
        else: 
            doc = {'_id': 'search', 'status': 'ready', 'new_users': new_users, 'result': 'Job submitted.', 'updated_at':time.ctime()}
            response = couch.upsertdoc('jobs/search', doc)
            return Response(response.json(), response.status_code)


    def start_stream(self):
        res = couch.get('jobs/stream')
        if res.status_code == 200 and res.json().get('status') != 'done':
            return Response(res.json(), 403)
        else: 
            doc = {'_id': 'stream', 'status': 'ready', 'result': 'Job submitted.', 'updated_at':time.ctime()}
            response = couch.upsertdoc('jobs/stream', doc)
            return Response(response.json(), response.status_code)
    
    def start_update(self):
        res = couch.get('jobs/update')
        if res.status_code == 200 and res.json().get('status') != 'done':
            return Response(res.json(), 403)
        else: 
            doc = {'_id': 'update', 'status': 'ready', 'result': 'Job submitted.', 'updated_at':time.ctime()}
            response = couch.upsertdoc('jobs/update', doc)
            return Response(response.json(), response.status_code)

    def calculate_user_rank(self):
        res = couch.get('jobs/user_rank')
        if res.status_code == 200 and res.json().get('status') != 'done':
            return Response(res.json(), 403)
        else: 
            doc = {'_id': 'user_rank', 'status': 'ready', 'result': 'Job submitted.', 'updated_at':time.ctime()}
            response = couch.upsertdoc('jobs/user_rank', doc)
            return Response(response.json(), response.status_code)

class ManagerViewSet(viewsets.ViewSet):

    # PUT analyser/manager/view_init
    @action(detail=False, methods=['put'], name="Initialisation CouchDB Views")
    def migrate_couchdb(self):
        res = couch.get('jobs/couchdb')
        if res.status_code == 200:
            return Response(res.json(), 403)
        else: 
            result = couch.migrate()
            doc = {'_id': 'couchdb', 'status': 'done', 'result': result, 'updated_at': time.ctime()}
            response = couch.upsertdoc('jobs/couchdb', doc)
            return Response(response.json(), response.status_code)

    # PUT analyser/manager/view_init
    @action(detail=False, methods=['put'], name="Initialisation CouchDB Views")
    def view_init(self, request):
        done = {}
        couch_path = os.path.join(settings.STATICFILES_DIRS[0], 'couch')
        for file_name in os.listdir(couch_path):
            if file_name.endswith("_view.json"):
                database = file_name.split('__')[0]
                view = file_name.split('__')[1]
                file_path = os.path.join(couch_path, file_name)
                with open(file_path, 'r') as f:
                    f = json.load(f)
                    couch.put(f'{database}/_design/{view}', body=f)
                done[database] = view
        return Response(done)


