from django.conf.urls import patterns, url

from phrases import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^recent/$', views.RecentView.as_view(), name='recent'),
    url(r'^popular/$', views.PopularView.as_view(), name='popular'),
    )

