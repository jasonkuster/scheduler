'''
Created on Aug 24, 2014

@author: Stuart Long
'''
from django.shortcuts import render
from django.http import HttpResponse
from course_scheduler.strings import Strings
from course_scheduler.models import *
from scheduler.course_scheduler.views.customEvent import EventForm
from django.views.decorators.csrf import ensure_csrf_cookie
import sys
import json

sys.path.append(Strings.SYSTEM_PATH_PREFIX + 'application/scheduler/cas/')
from checklogin import check_login
from checklogin import redirect_to_cas
import dateutil.parser
from dateutil import rrule

@ensure_csrf_cookie
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

def event_json(request):
    status, id, cookie = check_login(request, 'http://scheduler.acm.case.edu/scheduler/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://scheduler.acm.case.edu/scheduler/')
    if cookie != "":
        setcookie = True
    stu = Student.objects.get(case_id=id)
    enrolls = Enrollment.objects.filter(student__case_id=id)

    response_data = []
    for enroll in enrolls:
        event = Event.objects.get(id=enroll.event_id)
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)

        start_date = dateutil.parser.parse(start)
        end_date = dateutil.parser.parse(end)

        date_to_start = event.start_date if event.start_date > start_date.date() else start_date.date()
        date_to_end = event.end_date if event.end_date < end_date.date() else end_date.date()

        for dt in rrule.rrule(rrule.DAILY, dtstart=date_to_start, until=date_to_end):
            event_data = {}
            event_data['id'] = enroll.event_id
            try:
                event_data['title'] = event.meetingtime.meeting_class.dept + ' ' + str(event.meetingtime.meeting_class.class_number)
            except Exception:
                event_data['title'] = event.customevent.event_name
            event_data['allDay'] = False

            if "Su" in event.recur_type and dt.weekday() == 6:
                event_data['start'] = str(dt.date().isoformat()) + 'T' + str(event.start_time.isoformat())
                event_data['end'] = str(dt.date().isoformat()) + 'T' + str(event.end_time.isoformat())
            elif "M" in event.recur_type and dt.weekday() == 0:
                event_data['start'] = str(dt.date().isoformat()) + 'T' + str(event.start_time.isoformat())
                event_data['end'] = str(dt.date().isoformat()) + 'T' + str(event.end_time.isoformat())
            elif "Tu" in event.recur_type and dt.weekday() == 1:
                event_data['start'] = str(dt.date().isoformat()) + 'T' + str(event.start_time.isoformat())
                event_data['end'] = str(dt.date().isoformat()) + 'T' + str(event.end_time.isoformat())
            elif "W" in event.recur_type and dt.weekday() == 2:
                event_data['start'] = str(dt.date().isoformat()) + 'T' + str(event.start_time.isoformat())
                event_data['end'] = str(dt.date().isoformat()) + 'T' + str(event.end_time.isoformat())
            elif "Th" in event.recur_type and dt.weekday() == 3:
                event_data['start'] = str(dt.date().isoformat()) + 'T' + str(event.start_time.isoformat())
                event_data['end'] = str(dt.date().isoformat()) + 'T' + str(event.end_time.isoformat())
            elif "F" in event.recur_type and dt.weekday() == 4:
                event_data['start'] = str(dt.date().isoformat()) + 'T' + str(event.start_time.isoformat())
                event_data['end'] = str(dt.date().isoformat()) + 'T' + str(event.end_time.isoformat())
            elif "Sa" in event.recur_type and dt.weekday() == 5:
                event_data['start'] = str(dt.date().isoformat()) + 'T' + str(event.start_time.isoformat())
                event_data['end'] = str(dt.date().isoformat()) + 'T' + str(event.end_time.isoformat())
            else:
                continue
            response_data.append(event_data)

    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response