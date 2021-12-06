from datetime import timedelta
from utils.google_calendar.cal_setup import get_calendar_service
from utils import config as cfg

CALENDAR_ID = cfg.config[0]['google']["calendar_id"]


def createEvent(eventName, eventDate, EventLocation, EventDescription):
    service = get_calendar_service()

    data = eventDate
    start = data.isoformat()
    end = (data + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId=CALENDAR_ID, body={
        "summary": eventName,
        "description": EventDescription,
        "location": EventLocation,
        "start": {"dateTime": start, "timeZone": 'America/Sao_Paulo'},
        "end": {"dateTime": end, "timeZone": 'America/Sao_Paulo'}
    }
    ).execute()
    return event_result
