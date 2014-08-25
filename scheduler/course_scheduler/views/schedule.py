'''
Created on Aug 24, 2014

@author: Stuart Long
'''
from django.shortcuts import render
from django import forms
from django.core.exceptions import ValidationError
from course_scheduler.strings import Strings
import re
import sys

sys.path.append(Strings.SYSTEM_PATH_PREFIX + 'application/scheduler/cas/')
from checklogin import check_login
from checklogin import redirect_to_cas


def parse_time(array):
    timeArr = array.split('-')
    timeArr[0]=re.sub(r'( )+', "", timeArr[0])
    timeArr[1]=re.sub(r'( )+', "", timeArr[1])

    startTimeArr = timeArr[0].split(':')
    startTimeArr[1] = startTimeArr[1][:2]
    startTimeArr[0] = int(startTimeArr[0])
    startTimeArr[1] = int(startTimeArr[1])
    if 'pm' in timeArr[0] or 'PM' in timeArr[0]:
        if startTimeArr != 12:
            startTimeArr[0] = startTimeArr[0] + 12

    endTimeArr = timeArr[1].split(':')
    endTimeArr[1] = endTimeArr[1][:2]
    endTimeArr[0] = int(endTimeArr[0])
    endTimeArr[1] = int(endTimeArr[1])
    if 'pm' in timeArr[1] or 'PM' in timeArr[1]:
        if endTimeArr != 12:
            endTimeArr[0] = endTimeArr[0] + 12
    return startTimeArr, endTimeArr
    
def validate_time(value):
    validAMs = '([6-9]|10|11|12):[0-5][0-9](am|AM)'
    validPMs = '([1-9]|12):[0-5][0-9](pm|PM)'
    validTimes = '(' + validAMs + '( )*-( )*' + validAMs + ')|(' + validAMs + '( )*-( )*' + validPMs + ')|(' + validPMs + '( )*-( )*' + validPMs + ')'

    patt = re.compile(validTimes)
    if not patt.match(value):
        raise ValidationError('%s is not a valid time format!' % value)

    if not ""==(re.sub(validTimes, "", value)):
        raise ValidationError('%s is not a valid time format!' % value)

    startTimeArr, endTimeArr = parse_time(value)

    actSTime = startTimeArr[0] + startTimeArr[1] / 60.0
    actETime = endTimeArr[0] + endTimeArr[1] / 60.0

    if actSTime >= actETime:
        raise ValidationError('Start Time must be after end Time!')
    
def schedule(request):
    #check to see if the user is logged in
    #if not make the user login
    status, id, cookie = check_login(request, 'http://scheduler.acm.case.edu/scheduler/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://scheduler.acm.case.edu/scheduler/')
    if cookie != "":
        setcookie = True
        
    eventForm = EventForm()

    response = render(request, 'schedule.html', {'eventForm' : eventForm, 'id' : id})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response

class EventForm(forms.Form):
    event_title=forms.CharField(max_length=100)
    location=forms.CharField(max_length=100, required=False)
    times=forms.CharField(max_length=20, validators=[validate_time])
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