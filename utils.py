import requests
from config import Config


def send_webhook(resource_id, flat_list):
    try:
        resp = requests.post(Config.WEBHOOK_RECEIVER_URL, json={'resource_id': resource_id, 'data': flat_list}, headers={'Content-Type': 'application/json'})
        resp.raise_for_status()
    except Exception as e:
        pass
    else:
        return resp.status_code