from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.contrib import staticfiles

from . import view
 
urlpatterns = [
    url(r'^$', view.index),
]


