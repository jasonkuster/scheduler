from django.shortcuts import render
from course_scheduler.models import *
from course_scheduler.strings import Strings
from django.http import Http404
from django.db.models import Q
import random
import dateutil.parser
from dateutil import rrule

sys.path.append(Strings.SYSTEM_PATH_PREFIX + 'application/scheduler/cas/')
from checklogin import check_login
from checklogin import redirect_to_cas

def share(request):
    #check to see if the user is logged in
    #if not make the user login
    status, id, cookie = check_login(request, 'http://scheduler.acm.case.edu/scheduler/instructor/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://scheduler.acm.case.edu/scheduler/instructor/')
    if cookie != "":
        setcookie = True
    share_ids = Shares.objects.values_list('shareid', flat=True)
    rand = random.randint(1111111111, 9999999999)
    while rand in share_ids:
        rand = random.randint(1111111111, 9999999999)



#This function does no require login and
#checks the database for a shared schedule
#with the same share id it has, then displays
#the shared schedule.

def shareview(request, share):
    colors = ['#FF0000', '#32E01B', '#003CFF', '#FF9D00', '#00B7FF', '#9D00FF', '#FF00EA', '#B5AA59', '#79BF6B', '#CFA27E']

    classes = []
    toSend = {}
    shares = Shares.objects.filter(shareid=share)
    if shares == None:
        raise Http404

    for enroll in shares:
        event = Event.objects.get(id=enroll.event_id)
        top = event.start_time.hour - 6
        top += event.start_time.minute / 60.0
        top *= 75
        top += 135
        height = event.start_time.hour + (event.start_time.minute / 60.0)
        height = (event.end_time.hour + event.end_time.minute / 60.0) - height
        height *= 60
        height *= 1.2
        height += 3
        randColor = random.randint(0, len(colors)-1)
        color = colors[randColor] + ''
        del colors[randColor]
        toSend[event] = [top, height, color]
    response = render(request, 'view.html', {'events' : toSend})
    return response
