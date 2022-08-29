from utils import config as cfg
import requests
import json

def list_events(id):
    """
    Create an event in the discord API
    """
    try:
        discord_token = cfg.config[0]["discord"]["token"]
        guild_id = cfg.config[0]['discord']['guild']
        discord_api_version = cfg.config[0]['discord']['api_version']
        discord_base_url = cfg.config[0]['discord']['base_url']
        url = f"{discord_base_url}/{discord_api_version}/guilds/{guild_id}/scheduled-events/{id}"

        headers = {
            'Authorization': f"Bot {discord_token}",
            'Content-Type': 'application/json',
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)
    except Exception as e:
        print(f"Erro ao criar evento: {e}")
        return None

    return response.json()
