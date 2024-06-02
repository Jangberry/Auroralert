import requests
import datetime
import pytz

class AlertManager:
    dateformat = "%Y-%m-%d %H:%M %Z"

    def alert(self, probability = 0, location = (0, 0), date = datetime.datetime.now() + datetime.timedelta(minutes=30)):
        pass

class DiscordWebhookAlertManager(AlertManager):
    def __init__(self, url):
        self.url = url

    def alert(self, probability = 0, location = (0, 0), date = datetime.datetime.now() + datetime.timedelta(minutes=30)):
        # Send a message to the Discord webhook, with notification if probability is high
        if probability > 1:
            requests.post(self.url, json={"content": f"Aurora probability around **{date.astimezone(pytz.timezone('Europe/Paris')).strftime(DiscordWebhookAlertManager.dateformat)}** (*{date.strftime(AlertManager.dateformat)}*) next to `{location[1]}, {location[0]}` is **{probability}**" + (" @everyone" if probability > 10 else ""), "flags": (1 if probability < 3 else 0) << 12})

class SMSAlertManager(AlertManager):
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def alert(self, probability = 0, location = (0, 0), date = datetime.datetime.now() + datetime.timedelta(minutes=30)):
        # Send an SMS to the phone number, with notification if probability is high
        if probability > 3:
            requests.post("https://smsapi.free-mobile.fr/sendmsg", json={"user": self.user, "pass": self.password, "msg": f"Aurora probability around {date.astimezone(pytz.timezone('Europe/Paris')).strftime(AlertManager.dateformat)} next to {location} is {probability}"})