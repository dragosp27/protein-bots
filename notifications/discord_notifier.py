import requests
from .base import Notifier

class DiscordNotifier(Notifier):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def notify(self, message: str) -> None:
        payload = {"content": message}
        resp = requests.post(self.webhook_url, json=payload, timeout=5)
        resp.raise_for_status()