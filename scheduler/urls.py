'''
Created on Nov 14, 2012

@author: Stuart Long
'''

from django.conf.urls import patterns, url, include
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
	url(r'^$', lambda r : HttpResponseRedirect('scheduler/')),	
    url(r'^scheduler/$', 'course_scheduler.views.schedule.schedule', name='base'),
    url(r'^scheduler/customevent$', 'course_scheduler.views.customEvent.customevent', name='customevent'),
    url(r'^scheduler/view/(\d{10})$', 'course_scheduler.views.share.shareview', name='view'),
    url(r'^scheduler/search/$', 'course_scheduler.views.search.search', name='search'),
    url(r'^scheduler/add_course/$', 'course_scheduler.views.search.add_course', name='add_course'),
    url(r'^scheduler/remove_course/$', 'course_scheduler.views.search.remove_course', name='remove_course'),
    url(r'^scheduler/event_json$', 'course_scheduler.views.schedule.event_json', name='event_json'),
)
