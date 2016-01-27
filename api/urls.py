from django.conf.urls import patterns, include, url
from views import lesson_check, register, login


urlpatterns = patterns('',
    url(r'^check/([0-9]{1,3})$', lesson_check),
    url(r'^register/$', register),
    url(r'^login/$', login),
)
