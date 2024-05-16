import Alert
import requests
import datetime
import config

class MeshData:
    def __init__(self, raw) -> None:
        self.observation_time = datetime.datetime.fromisoformat(raw['Observation Time'][:-1]+'+00:00')
        self.forecast_time = datetime.datetime.fromisoformat(raw['Forecast Time'][:-1]+'+00:00')
        # "[Longitude, Latitude, Aurora]" => ["Longitude", "Latitude", "Aurora"]
        raw['Data Format'] = raw['Data Format'][1:-1].split(', ')
        self.data = map(lambda x: {raw['Data Format'][0]: x[0], raw['Data Format'][1]: x[1], raw['Data Format'][2]: x[2]}, raw['coordinates'])

    def __getitem__(self, key):
        return self.data[key]
    
    def __iter__(self):
        return iter(self.data)

def main():
    alerts = [
        Alert.DiscordWebhookAlertManager(config.Discord['webhookURL']),
        Alert.SMSAlertManager(config.SMS['user'], config.SMS['pass'])
        ]
    r = requests.get('https://services.swpc.noaa.gov/json/ovation_aurora_latest.json')
    data = MeshData(r.json())

    for point in data:
        if point['Latitude'] == round(config.POI['Latitude']) and point['Longitude'] == round(config.POI['Longitude']):
            for alert in alerts:
                alert.alert(point['Aurora'], (point['Latitude'], point['Longitude']), data.forecast_time)
    
    import os.path
    if not os.path.exists('Auroralert.service') or not os.path.exists('Auroralert.timer'):
        print(f"To enable auto alerts (run {os.path.realpath(__file__)} every {int(config.checkInterval)} minutes), run the following commands:")
        print("ln -s Auroralert.service Auroralert.timer ~/.config/systemd/user/")
        print("systemctl --user enable Auroralert.timer")
        print("systemctl --user start Auroralert.timer")
    
    with open('Auroralert.service', 'w') as f:
        f.write(f'''[Unit]
Description=Watch for Aurora events
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory={os.path.dirname(os.path.realpath(__file__))}
ExecStart=/usr/bin/python3 {os.path.realpath(__file__)}
''')
    
    with open('Auroralert.timer', 'w') as f:
        f.write(f'''[Unit]
Description=Watch for Aurora events

[Timer]
OnCalendar=*-*-* *:0/{int(config.checkInterval)}
Persistent=true

[Install]
WantedBy=timers.target
''')

if __name__ == "__main__":
    main()