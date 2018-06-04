from django.conf.urls import url
from . import views
           
urlpatterns = [
        url(r'^$',views.index),
        url(r'^register$',views.register),
        url(r'^login$',views.login),
        url(r'^home$',views.home),
        url(r'^logout$', views.logout),
        url(r'^add_job$', views.add_job), 
        url(r'^show/(?P<id>\d+)/$', views.show),
        url(r'^edit/(?P<id>\d+)/$', views.edit),
        url(r'^edit_page/(?P<id>\d+)/$', views.edit_page),
        url(r'^add_to_myjob/(?P<id>\d+)/$', views.add_to_myjob),            
        url(r'^add_job_form$', views.add_job_form),
        url(r'^remove/(?P<id>\d+)$', views.remove),     
    ]