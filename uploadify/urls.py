try:
    # Django 1.6.0
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from uploadify.views import *

urlpatterns = patterns('',
    url(r'upload/$', upload, name='uploadify_upload'),
)
