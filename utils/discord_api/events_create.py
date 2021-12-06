from utils import config as cfg
import requests
import json


def create_event(name, description, start_time):
    """
    Create an event in the discord API
    """
    url = f"https://discordapp.com/api//guilds/{cfg.config[0]['discord']['guild']}/scheduled-events"

    payload = json.dumps({
    "name": name,
    "description": description,
    "privacy_level": 2,
    "scheduled_start_time": start_time,
    "entity_type": 2,
    "channel_id": f"{cfg.config[0]['discord']['voice_channel_id']}",
    })
    headers = {
    'Authorization': f"Bot {cfg.config[0]['discord']['token']}",
    'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return  response.status_code
