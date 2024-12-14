import requests
from django.conf import settings


class CentrifugoClient:
    def __init__(self, api_url=None, api_key=None):
        self.api_url = api_url or settings.CENTRIFUGO_API_URL
        self.api_key = api_key or settings.CENTRIFUGO_API_KEY

    def _request(self, method, params):
        data = {
            "method": method,
            "params": params
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"apikey {self.api_key}"
        }
        response = requests.post(self.api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def publish(self, channel, data):
        return self._request("publish", {"channel": channel, "data": data})

    def broadcast(self, channels, data):
        return self._request("broadcast", {"channels": channels, "data": data})

    def unsubscribe(self, channel, user):
        return self._request("unsubscribe", {"channel": channel, "user": user})

    def disconnect(self, user):
        return self._request("disconnect", {"user": user})

    def presence(self, channel):
        return self._request("presence", {"channel": channel})

    def presence_stats(self, channel):
        return self._request("presence_stats", {"channel": channel})

    def history(self, channel, limit=0, since=None, reverse=False):
        params = {"channel": channel, "limit": limit, "reverse": reverse}
        if since:
            params["since"] = since
        return self._request("history", params)

    def history_remove(self, channel):
        return self._request("history_remove", {"channel": channel})

    def channels(self):
        return self._request("channels", {})

    def info(self):
        return self._request("info", {})
