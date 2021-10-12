import datetime
from utils.google_calendar.cal_setup import get_calendar_service
from utils import config as cfg
import logging
from dateutil import tz

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def getEvents():
   service = get_calendar_service()
   # Call the Calendar API
   dt = datetime.datetime.now(tz=cfg.TZ)
   BR = tz.gettz('America/Sao_Paulo')  
   start_date = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0, 00,0 ,tzinfo=BR).isoformat() 
   end_date = datetime.datetime(dt.year,  dt.month,  dt.day, 23, 30, 59, 0,tzinfo=BR).isoformat() 

   events_result = service.events().list(
       calendarId='iici0lagcvqc7dtarsjpqmg00c@group.calendar.google.com', timeMin=start_date, timeMax=end_date,
       maxResults=10, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])
   return events

def getEventsWeek():
   service = get_calendar_service()
   # Call the Calendar API
   
   dt = datetime.datetime.now(tz=cfg.TZ)
   week_number = dt.isocalendar()[1]
   firstdayofweek = datetime.datetime.strptime(f'{dt.year}-W{int(week_number)}-1', "%Y-W%W-%w").date()
   lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)

   BR = tz.gettz('America/Sao_Paulo')  
   start_date = datetime.datetime(firstdayofweek.year, firstdayofweek.month, firstdayofweek.day, 6, 0, 00,0 ,tzinfo=BR).isoformat() 
   end_date = datetime.datetime(lastdayofweek.year,  lastdayofweek.month,  lastdayofweek.day, 23, 30, 59, 0,tzinfo=BR).isoformat() 

   events_result = service.events().list(
       calendarId='iici0lagcvqc7dtarsjpqmg00c@group.calendar.google.com', timeMin=start_date, timeMax=end_date,
       maxResults=10, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])
   return events
