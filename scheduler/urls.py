'''
Created on Nov 14, 2012

@author: Stuart Long
'''

from django.conf.urls import patterns, url, include
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
	url(r'^$', lambda r : HttpResponseRedirect('scheduler/')),	
    url(r'^scheduler/$', 'course_scheduler.views.schedule.schedule', name='base'),
    url(r'^scheduler/login', 'course_scheduler.views.old_views.login', name='login'),
    url(r'^scheduler/customevent$', 'course_scheduler.views.old_views.customevent', name='customevent'),
    url(r'^scheduler/about$', 'course_scheduler.views.old_views.about', name='about'),
    url(r'^scheduler/view/(\d{10})$', 'course_scheduler.views.old_views.shareview', name='view'),
    url(r'^scheduler/searchtest$', 'course_scheduler.views.old_views.searchtest', name='searchtest'),
    url(r'^scheduler/search/$', 'course_scheduler.views.search.search', name='search'),
    url(r'^scheduler/add_course/$', 'course_scheduler.views.search.add_course', name='add_course'),
    url(r'^scheduler/remove_course/$', 'course_scheduler.views.search.remove_course', name='remove_course'),
	url(r'^scheduler/calendar_test/$', 'course_scheduler.views.old_views.calendar_test', name='calendar_test'),
    url(r'^scheduler/event_json$', 'course_scheduler.views.old_views.event_json', name='event_json'),
)
