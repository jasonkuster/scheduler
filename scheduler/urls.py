'''
Created on Nov 14, 2012

@author: Stuart Long
'''

from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^scheduler/$', 'course_scheduler.views.old_views.schedule', name='base'),
    url(r'^scheduler/add/$', 'course_scheduler.views.old_views.add', name='add'),
    url(r'^scheduler/info$', 'course_scheduler.views.old_views.info', name='info'),
    url(r'^scheduler/instructor$', 'course_scheduler.views.old_views.instructor', name='instructor'),
    url(r'^scheduler/login', 'course_scheduler.views.old_views.login', name='login'),
    url(r'^scheduler/inscourse$', 'course_scheduler.views.old_views.inscourse', name='inscourse'),
    url(r'^scheduler/inssearch$', 'course_scheduler.views.old_views.inssearch', name='insearch'),
    url(r'^scheduler/addcourse$', 'course_scheduler.views.old_views.addcourse', name='addcourse'),
    url(r'^scheduler/removecourse$', 'course_scheduler.views.old_views.removecourse', name='removecourse'),
    url(r'^scheduler/mycourses$', 'course_scheduler.views.old_views.mycourses', name='mycourses'),
    url(r'^scheduler/customevent$', 'course_scheduler.views.old_views.customevent', name='customevent'),
    url(r'^scheduler/about$', 'course_scheduler.views.old_views.about', name='about'),
    url(r'^scheduler/view/(\d{10})$', 'course_scheduler.views.old_views.shareview', name='view'),
    url(r'^scheduler/searchtest$', 'course_scheduler.views.old_views.searchtest', name='searchtest'),
    url(r'^scheduler/search/$', 'course_scheduler.views.search.search', name='search'),
    url(r'^scheduler/add_course/$', 'course_scheduler.views.search.add_course', name='add_course'),
    url(r'^scheduler/remove_course/$', 'course_scheduler.views.search.remove_course', name='remove_course'),
)
