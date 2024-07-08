import json
import os
from .utils import get_default_download_dir

class Settings:
    def __init__(self):
        self.settings_file = os.path.expanduser("~/.fridapatcher_settings.json")
        self.settings = self.load_settings()
        self.save_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return {
            "auto_install": {
                "enabled": False,
                "ios_ip": "",
                "ios_port": ""
            },
            "proxy": {
                "enabled": False,
                "type": "http",
                "ip": "",
                "port": "",
                "username": "",
                "password": ""
            },
            "download_dir": get_default_download_dir()
        }

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, key):
        return self.settings.get(key)

    def update_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()