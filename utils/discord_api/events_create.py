from utils import config as cfg
import requests
import json


def create_event(name, description, start_time):
    """
    Create an event in the discord API
    """
    try:
        discord_token = cfg.config[0]["discord"]["token"]
        guildId = cfg.config[0]['discord']['guild']
        discord_api_version = cfg.config[0]['discord']['api_version']
        discord_base_url = cfg.config[0]['discord']['base_url']
        voice_channel_id = cfg.config[0]['discord']['voice_channel_id']
        url = f"{discord_base_url}/{discord_api_version}/guilds/{guildId}/scheduled-events"

        payload = json.dumps({
            "name": name,
            "description": name,
            "privacy_level": 2,
            "scheduled_start_time": start_time,
            "entity_type": 2,
            "channel_id": voice_channel_id
            })
        headers = {
            'Authorization': f"Bot {discord_token}",
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)

    except Exception as e:
        print(f"Erro ao criar evento: {e}")
        print(url)
        return None

    return response
