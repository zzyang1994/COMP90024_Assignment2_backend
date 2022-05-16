import json

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .data.data import *
import couchdb
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getData(request):
    tmp = {'msg': 'hello'}
    return Response(tmp)


# Create your views here.
@csrf_exempt
def get_line_data(request):
    suburbs = []
    index = 0
    while (True):

        sub = request.GET.get(f'sub{index}')
        if (sub == None):
            break
        index += 1
        suburbs.append(sub)

    print(suburbs)
    t = {"data": {}, "msg": "Success"}
    t['data']['data'], t['data']['date_list'] = suburb_line_data(suburbs)
    return JsonResponse(t)

@csrf_exempt
def get_line_data_historical(request):
    suburbs = []
    index = 0
    while (True):

        sub = request.GET.get(f'sub{index}')
        if (sub == None):
            break
        index += 1
        suburbs.append(sub)

    print(suburbs)
    t = {"data": {}, "msg": "Success"}
    t['data']['data'], t['data']['date_list'] = suburb_line_data(suburbs, "Historical")
    return JsonResponse(t)

@csrf_exempt
def get_word_cloud(request):
    indicator = request.GET.get('indicator')
    t = {"data": {}, "msg": "Success"}
    t['data'] = suburb_wordcloud_data(indicator)
    return JsonResponse(t)

@csrf_exempt
def get_suburb(request):
    time = request.GET.get('time')
    return JsonResponse({"data": suburbs(time), "msg": ""})

@csrf_exempt
def getfields_traffic(request):
    t = {'data': get_fields("traffic"), 'msg': ''}
    return JsonResponse(t)


@csrf_exempt
def getfields_healthy(request):
    t = {'data': get_fields("healthy"), 'msg': ''}
    return JsonResponse(t)


@csrf_exempt
def getdata_traffic_bar(request):
    data = get_bar_chart_traffic()
    t = {'data': {
        'fields': data[0],
        'bar_data': data[1]
    },
        'msg': ''}
    return JsonResponse(t)


@csrf_exempt
def getdata_healthy_bar(request):
    data = get_bar_chart_healthy()
    t = {'data': {
        'fields': data[0],
        'bar_data': data[1]
    },
        'msg': ''}
    return JsonResponse(t)


@csrf_exempt
def get_pie_data_traffic(request):
    indicator = request.GET.get('indicator')
    t = {'data': [], 'msg': ''}

    try:
        t['data'] = get_pie_chart_traffic(indicator)
        t['msg'] = 'Success'
    except:
        t['msg'] = 'Fail'

    return JsonResponse(t)


@csrf_exempt
def get_pie_data_healthy(request):
    indicator = request.GET.get('indicator')
    t = {'data': [], 'msg': ''}

    try:
        t['data'] = get_pie_chart_healthy(indicator)
        t['msg'] = 'Success'
    except:
        t['msg'] = 'Fail'

    return JsonResponse(t)


@csrf_exempt
def mapdata(request):
    return JsonResponse(get_map_data())

@csrf_exempt
def mapGeoData(request):
    return JsonResponse(get_map_geoData())
