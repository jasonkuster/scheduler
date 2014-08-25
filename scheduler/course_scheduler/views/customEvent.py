'''
Created on Aug 24, 2014

@author: Stuart Long
'''
from django.shortcuts import render
from django import forms
from course_scheduler.strings import Strings
from django.http import HttpResponseRedirect
from course_scheduler.models import *
import datetime
from django.views.decorators.csrf import csrf_protect
import sys

sys.path.append(Strings.SYSTEM_PATH_PREFIX + 'application/scheduler/cas/')
from checklogin import check_login
from checklogin import redirect_to_cas

@csrf_protect
def customevent(request):
    #check to see if the user is logged in
    #if not make the user login
    status, id, cookie = check_login(request, 'http://scheduler.acm.case.edu/scheduler/instructor/')
    if status == False:
        return redirect_to_cas('http://scheduler.acm.case.edu/scheduler/instructor/')

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['event_title']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            sdate = form.cleaned_data['start_date']
            edate = form.cleaned_data['end_date']

            try:
                loc = form.cleaned_data['location']
            except:
                loc = ""

            dayStr = ''
            if form.cleaned_data['su']:
                dayStr += 'Su'
            if form.cleaned_data['m']:
                dayStr += 'M'
            if form.cleaned_data['tu']:
                dayStr += 'Tu'
            if form.cleaned_data['w']:
                dayStr += 'W'
            if form.cleaned_data['th']:
                dayStr += 'Th'
            if form.cleaned_data['f']:
                dayStr += 'F'
            if form.cleaned_data['sa']:
                dayStr += 'Sa'

            #event = CustomEvent(start_time=datetime.time(startTimeArr[0], startTimeArr[1]), end_time=datetime.time(endTimeArr[0], endTimeArr[1]), recur_type=days, event_name=name)
            event = CustomEvent(start_time=datetime.time(start_time, end_time), end_time=datetime.time(endTimeArr[0], endTimeArr[1]), start_date=sdate, end_date=edate, recur_type=dayStr, event_name=name, location=loc)
            event.save()

            stu = Student.objects.get(case_id=id)
            enroll = Enrollment(student_id=stu.pk, event_id=event.id)
            enroll.save()

    return HttpResponseRedirect('/scheduler/')
    


class EventForm(forms.Form):
    event_title=forms.CharField(max_length=100)
    location=forms.CharField(max_length=100, required=False)
    start_time=forms.CharField(max_length=20)
    end_time=forms.CharField(max_length=20)
    start_date=forms.DateField()
    end_date=forms.DateField()
    #days=forms.CharField(max_length=14, validators=[validate_day])
    CHOICES=((0,'M'),(0,'Tu'),(0,'W'),(0,'Th'),(0,'F'),(0,'Sa'),(0,'Su'))
    m = forms.BooleanField(label="day", required=False)
    tu = forms.BooleanField(label="day", required=False)
    w = forms.BooleanField(label="day", required=False)
    th = forms.BooleanField(label="day", required=False)
    f = forms.BooleanField(label="day", required=False)
    sa = forms.BooleanField(label="day", required=False)
    su = forms.BooleanField(label="day", required=False)