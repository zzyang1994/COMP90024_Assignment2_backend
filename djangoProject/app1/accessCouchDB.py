## ----- get data from couchdb
import couchdb
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def getRawData():
    couch = couchdb.Server('http://admin:password@115.146.95.1:5984/')

    db = couch['comp90024-group21']

    db.save({"messi": "0"})

    return HttpResponse("Welcome Messi~")

getRawData();