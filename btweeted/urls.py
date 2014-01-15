from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('phrases.urls', namespace="phrases")), # phrases app is the homepage.
    url(r'^admin/', include(admin.site.urls)),
)
