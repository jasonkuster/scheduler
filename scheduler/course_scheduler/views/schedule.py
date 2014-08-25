'''
Created on Aug 24, 2014

@author: Stuart Long
'''
from django.shortcuts import render
from django import forms
from django.core.exceptions import ValidationError
from course_scheduler.strings import Strings
from django.http import HttpResponseRedirect
from course_scheduler.models import *
import course_scheduler.views.customEvent.EventForm
import datetime
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import re
import sys

sys.path.append(Strings.SYSTEM_PATH_PREFIX + 'application/scheduler/cas/')
from checklogin import check_login
from checklogin import redirect_to_cas

def schedule(request):
    #check to see if the user is logged in
    #if not make the user login
    status, id, cookie = check_login(request, 'http://scheduler.acm.case.edu/scheduler/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://scheduler.acm.case.edu/scheduler/')
    if cookie != "":
        setcookie = True
        
    eventForm = course_scheduler.views.customEvent.EventForm()

    response = render(request, 'schedule.html', {'eventForm' : eventForm, 'id' : id})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response