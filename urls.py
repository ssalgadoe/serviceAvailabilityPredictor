from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    #path('', views.index, name='index'),
    path('home', views.home, name='home'),
    url(r'customer/(?P<cust_id>.+)/(?P<select_id>.+)/$',views.customer, name='customer'),
    url(r'^(?P<select_id>.+)/$',views.index, name='index'),
    path('', views.index, name='index'),
    ]