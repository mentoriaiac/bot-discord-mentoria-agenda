from datetime import datetime, timedelta
from utils.google_calendar.cal_setup import get_calendar_service
import logging

#logging.basicConfig(level=logging.DEBUG)

def createEvent(eventName, eventDate, EventLocation, EventDescription):
   service = get_calendar_service()

   data = eventDate 
   start = data.isoformat()
   end = (data + timedelta(hours=1)).isoformat()

   event_result = service.events().insert(calendarId='iici0lagcvqc7dtarsjpqmg00c@group.calendar.google.com',
       body={
           "summary": eventName,
           "description": EventDescription,
           "location": EventLocation,
           "start": {"dateTime": start, "timeZone": 'America/Sao_Paulo'},
           "end": {"dateTime": end, "timeZone": 'America/Sao_Paulo'}   
            }
   ).execute()
   return event_result
