'''
Created on Aug 17, 2014

@author: Stuart Long
'''

from django.shortcuts import render
from course_scheduler.models import *
from course_scheduler.strings import Strings
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.db.models import Q
from checklogin import check_login
from checklogin import redirect_to_cas
import json
import re
import string

#TODO smarter search
@ensure_csrf_cookie
def search(request):
    status, id, cookie = check_login(request, 'http://scheduler.acm.case.edu/scheduler/searchtest/')
    toSend = {}
    criterion = ''   
    
    if request.method == 'GET':  
        ##checking if it matches something like EECS 132
        patt = re.compile('(\w{4}( )*(\d{1,4}|(\d{1.4}w)))')
        criterion = request.GET['criterion']
        originalCriterion = criterion;
        criterion = criterion.strip()
        
        
        if patt.match(criterion):
            str = string.replace(criterion, ' ', '')
            arr = [None]*2
            arr[0] = str[0:3]
            arr[1] = str[4:]
            classes = Instructs.objects.filter(meeting__meeting_class__dept__icontains=arr[0], meeting__meeting_class__class_number__istartswith=arr[1])
        else:
            classes = Instructs.objects.filter(Q(meeting__meeting_class__classname__icontains=criterion)
                                            | Q(meeting__meeting_class__dept__icontains=criterion)
                                            | Q(meeting__meeting_class__class_number__icontains=criterion)
                                            | Q(instructor__name__icontains=criterion))

        for c in classes:
            if Enrollment.objects.filter(student_id=id, event_id=c.meeting.id).exists():
                toSend[c] = True
            else:
                toSend[c] = False
    else:
        return HttpResponseBadRequest('Search Failed')
    
    response = render(request, 'search_result.html', {'classes' : toSend, 'searchid' : originalCriterion, 'student_id' : id})
    return response

@csrf_protect
def add_course(request):
    if request.method == 'POST':
        eventId = request.POST['eventID']
        caseId = request.POST['studentID']
        stu = Student.objects.get(case_id=caseId)
        enroll = Enrollment(student_id=stu.pk, event_id=eventId)
        enroll.save()
        responseData = {}
        responseData['eventID'] = eventId
        responseData['studentID'] = caseId
        return HttpResponse(json.dumps(responseData), content_type='application/json')
        #return HttpResponse('Success', content_type='text/plain')
    return HttpResponseBadRequest('Add Failed')

@csrf_protect
def remove_course(request):
    if request.method == 'POST':
        eventId = request.POST['eventID']
        caseId = request.POST['studentID']
        stu = Student.objects.get(case_id=caseId)
        enroll = Enrollment.objects.get(student_id=stu.pk, event_id=eventId)
        enroll.delete()
        responseData = {}
        responseData['eventID'] = eventId
        responseData['studentID'] = caseId
        return HttpResponse(json.dumps(responseData), content_type='application/json')
    return HttpResponseBadRequest('Remove Failed')