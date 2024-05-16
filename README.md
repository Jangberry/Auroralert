# Auroralert

Really quick script to get notification on the next aurora borealis (really hated the fact that I missed it on the 10th of may 2024).

## Installation

```bash
git clone https://github.com/jangberry/auroralert
cd auroralert
pip install -r requirements.txt
```

Set some custom values in `config.py`:

```python
Discord = {"webhookURL": "https://discord.com/api/webhooks/<the path you'll get in Discord>"}
SMS = {"user": "<FreeMobile user ID>", "pass": "<get it on https://mobile.free.fr/account/mes-options/notifications-sms>"}
POI = {
    'Latitude': <your lat>,
    'Longitude': <your long>
}
checkInterval = 5 # That's an int representing the number of minutes between each check
```

## Usage

```bash
python auroralert.py
# It will just run, and create timers to check the aurora borealis every `checkInterval` minutes, you'll then need to run
ln -L /path/to/auroralert/Auroralert.timer /path/to/auroralert/Auroralert.service ~/.config/systemd/user/
systemctl --user enable Auroralert.timer
systemctl --user start Auroralert.timer
```
