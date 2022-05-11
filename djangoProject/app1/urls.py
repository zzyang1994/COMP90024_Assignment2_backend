from django.urls import include, re_path
from app1 import views

urlpatterns = [
    # url(r'^api/getData$', views.getData),
    # url(r'^api/index$', views.index),
    re_path(r'^overview/pie/traffic$', views.get_pie_data_traffic),
    re_path(r'^overview/pie/healthy$', views.get_pie_data_healthy),
    re_path(r'^overview/bar/traffic$', views.getdata_traffic_bar),
    re_path(r'^overview/bar/healthy$', views.getdata_healthy_bar),
    re_path(r'^overview/line$', views.get_line_data),
    re_path(r'^overview/wordCloud$', views.get_word_cloud),
    re_path(r'^map/$', views.mapdata),
    re_path(r'^fields/traffic$', views.getfields_traffic),
    re_path(r'^fields/healthy$', views.getfields_healthy),
    re_path(r'^fields/suburb$', views.get_suburb),
]