#!/usr/bin/env python

from bs4 import BeautifulSoup
from course_scheduler.models import Class, MeetingTime, Instructor, Instructs, Event, Term
import course_scheduler
import sys
import re
import urllib2

def add_twelve_hours(time):
    """Make time into PM.  Requires time in format 'XX:YY'"""
    time_hour = time.split(":")[0]
    time_minute = time.split(":")[1].split(" ")[0]
    if int(time_hour) != 12:
        time_hour = int(time_hour) + 12
    time = str(time_hour) + ":" + time_minute
    return time

def format_date(date):
    """Turns a date in XX/YY/ZZZZ into ZZZZ-XX-YY.  Needed for python's Date"""
    parts = [part.strip() for part in date.split("/")]
    return "-".join([parts[2],parts[0],parts[1]])

def format_times(s_time, e_time):
    """Turns '12:30 - 2:30 PM' into ('12:30','14:30').
    Needed for python's Time field"""
    if "PM" in e_time:
        e_time = add_twelve_hours(e_time)
        s_hour = s_time.strip().split(":")[0]
        e_hour = e_time.strip().split(":")[0]
        if int(e_hour) - int(s_hour) > 6:
            s_time = add_twelve_hours(s_time)

    elif "PM" in s_time:
        s_time = add_twelve_hours(s_time)

    if "AM" in s_time or "PM" in s_time:
        s_time = s_time.strip().split(" ")[0]

    if "AM" in e_time or "PM" in e_time:
        e_time = e_time.strip().split(" ")[0]

    return (s_time, e_time)

def main(opened_file):

    xml_file = ""
# read entire file as string into xml_file
    xml_file += opened_file.read()

    print 'file opened'

# parse entire file as XML into a beautifulsoup object.

    b = BeautifulSoup(xml_file, "lxml")

    print 'file parsed'

# for every term, for every class, add the class

    for curr_term in b.find_all('term'):
        classes = curr_term.classes.find_all('class')
        term_name = curr_term.descr.contents[0].encode('utf-8')

        semester, year = term_name.split()
        if semester == 'Spring':
            semester = 'S'
        elif semester == 'Fall':
            semester = 'F'
        elif semester == 'Summer':
            semester = 'U'
        term_model = Term(term_id=int(curr_term['code']), name=semester + str(year))
        print semester + str(year)
        term_model.save()

        for c in classes:
            try:
                c_num = c.catalognbr.contents[0]
                print c_num
                d = c.subject.contents[0].encode('utf-8')
                name = c.coursetitlelong.contents[0].encode('utf-8')
                try:
                    desc = c.description.contents[0].encode('utf-8')
                except AttributeError:
                    try:
                        desc = c.classnotes.contents[0].encode('utf-8')
                    except AttributeError:
                        desc = ""

                try:
                    c_num = int(re.search(r'\d+', c_num).group())
                except Exception:
                    c_num = int(c_num)
                if len(desc) > 4096:
                    desc = desc[:4095]
                c_model = Class(class_number=c_num, dept=d, classname=name, description=desc, term=term_model)
                c_model.save()
            except ValueError,UnicodeEncodeError:
                # if they have non-unicode characters in their description, we don't add it to the DB.
                continue


# if there are meetings, find and add them.  If there are no meetings, don't add any.

            try:
                meetings = c.meetings.find_all('meeting')
            except AttributeError:
                continue

            for meeting in meetings:
                dates = meeting.meetingdates.contents[0]
                times = meeting.daystimes.contents[0]
                room = unicode(meeting.room.contents[0])
                s_date = dates.split("-")[0].strip()
                e_date = dates.split("-")[1].strip()
                weekdays = times.split(" ")[0]
                try:
                    s_time = times.split(" ")[1].strip()
                    e_time = times.split("-")[1].strip()
                    s_time, e_time = format_times(s_time, e_time)
                    if s_time == "" or e_time == "":
                        continue
                except IndexError:
                    continue

                s_date = format_date(s_date)
                e_date = format_date(e_date)

                m = MeetingTime(meeting_class = c_model, meeting_location = room, start_date = s_date, end_date = e_date, recur_type = weekdays, start_time = s_time, end_time = e_time)
                m.save()

                insts = unicode(meeting.instructor.contents[0])
                # instructor names are in format like 'inst1,inst2,inst3'.
                for inst_name in insts.split(","):
                    inst, created = Instructor.objects.get_or_create(name=inst_name)
                    instructs = Instructs(instructor=inst, meeting = m)
                    instructs.save()

if __name__ == "__main__":
    try:
        opened_file = open(sys.argv[1])
    except Exception:
        opened_file = urllib2.urlopen('http://case.edu/projects/erpextract/soc.xml')
    main(opened_file)
