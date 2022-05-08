from django.conf.urls import url
from app1 import views

urlpatterns = [
    # url(r'^api/getData$', views.getData),
    # url(r'^api/index$', views.index),
    url(r'^overview/pie/traffic$', views.get_pie_data_traffic),
    url(r'^overview/pie/healthy$', views.get_pie_data_healthy),
    url(r'^overview/bar/traffic$', views.getdata_traffic_bar),
    url(r'^overview/bar/healthy$', views.getdata_healthy_bar),
    url(r'^overview/line$', views.get_line_data),
    url(r'^map/$', views.mapdata),
    url(r'^fields/traffic$', views.getfields_traffic),
    url(r'^fields/healthy$', views.getfields_healthy),
    url(r'^fields/suburb$', views.get_suburb),
]