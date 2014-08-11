from django.conf.urls import patterns, url
from dictionary import views

urlpatterns = patterns('',
                       url(r'^$',views.index,name='index'),
                        url(r'^index/$',views.index,name='index'),
                       url(r'^login$',views.login,name='login'),
                       url(r'^logout$',views.logout,name='logout'),
                       url(r'^search/$',views.search,name='search')
                       )

