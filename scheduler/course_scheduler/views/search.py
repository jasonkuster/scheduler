from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import *
from course_scheduler.strings import Strings
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.exceptions import ValidationError
import datetime
import re
import sys
import random
import string
import logging


sys.path.append(Strings.SYSTEM_PATH_PREFIX + 'application/scheduler/cas/')
from checklogin import check_login
from checklogin import redirect_to_cas

def search(request)
    #logging.debug('GOT A REQUEST')
    toSend = {}
    if request.method == 'GET'
        #logging.debug('IT IS A GET')
        #criterion = request.GET.get('Search', None)
        #TODO better regexes
        #patt = re.compile('(wwww ((www)(wwww)))(wwwwwww)')
##       patt = re.compile('(wwww( )(d+(d+w)))')
        criterion = request.GET['criterion']
##        if patt.match(criterion)
##            str = string.replace(criterion, ' ', '')
##            arr = [None]2
##            arr[0] = str[03]
##            arr[1] = str[4]
##            #arr = criterion.split(' ')
##            classes = Instructs.objects.filter(meeting__meeting_class__dept__icontains=arr[0], meeting__meeting_class__class_number__icontains=arr[1])
##        else

        response = render(request, 'add.html', {'classes' : toSend, 'id' : id, 'form' : SearchForm()})
        classes = Instructs.objects.filter(Q(meeting__meeting_class__classname__icontains=criterion) |
                                           Q(meeting__meeting_class__dept__icontains=criterion) |
                                           Q(meeting__meeting_class__class_number__icontains=criterion) |
                                           Q(meeting__meeting_class__instructor__icontains=criterion))

        for c in classes
            toSend[c.pk] = False
##            if Enrollment.objects.filter(student_id=id, event_id=c.meeting.id).exists()
##                toSend[c] = True
##            else
##                toSend[c] = False
    else
        return None

    response_data = {}
    response_data['courses'] = classes
    response_data['in_schedule'] = toSend
    response_data['criterion'] = criterion
    response = HttpResponse(json.dumps(response_data), content_type="application/json")
   ## response = render(request, 'search_result.html', {'classes'  toSend})
    #logging.debug('RETURNING')
    return response
