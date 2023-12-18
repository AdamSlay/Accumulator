import os
import toml
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz


class Config:
    def __init__(self):
        # Check if .env file exists
        if os.path.exists('.env'):
            load_dotenv()
        # load example .env file if .env file does not exist(for testing)
        elif os.path.exists('.env.example'):
            load_dotenv('.env.example')
        else:
            raise FileNotFoundError("The .env file was not found.")

        # Set environment variables as attributes
        for key, value in os.environ.items():
            setattr(self, key, self._convert_to_int(value))

        # Check if config.toml file exists
        if os.path.exists('etc/config/config.toml'):
            config = toml.load('etc/config/config.toml')
            for key, value in config['settings'].items():
                setattr(self, key, self._convert_to_int(value))
        else:
            raise FileNotFoundError("The config.toml file was not found.")

        # Set the time stamp for the most recent hour
        now_utc = datetime.now(pytz.timezone('UTC'))
        if now_utc.minute <= 5:
            now_utc = now_utc - timedelta(hours=1)
        self.DATE_TIME = now_utc.strftime('%Y-%m-%d %H:00:00')

    @staticmethod
    def _convert_to_int(value):
        # If the value is a string and is numeric, convert it to an integer
        return int(value) if isinstance(value, str) and value.isdigit() else value