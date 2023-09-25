import os
import toml
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz


class Config:
    def __init__(self):
        # Load variables from .env file
        load_dotenv()

        # Set environment variables as attributes
        for key, value in os.environ.items():
            setattr(self, key, self._convert_to_int(value))

        # Load variables from config.toml file
        config = toml.load('etc/config/config.toml')
        for key, value in config['settings'].items():
            setattr(self, key, self._convert_to_int(value))

        # Set the time stamp for the most recent hour
        now_utc = datetime.now(pytz.timezone('UTC'))
        if now_utc.minute <= 5:
            now_utc = now_utc - timedelta(hours=1)
        self.DATE_TIME = now_utc.strftime('%Y-%m-%d %H:00:00')

    @staticmethod
    def _convert_to_int(value):
        # If the value is a string and is numeric, convert it to an integer
        return int(value) if isinstance(value, str) and value.isdigit() else value
