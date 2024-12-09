import json
import os


class AllConf:
    # read from app_credentials.json
    if os.path.exists('app_credentials.json'):
        with open('app_credentials.json') as f:
            app_credentials = json.load(f)
            SECRET_KEY = app_credentials.get(
                'SECRET_KEY') or ''
            NEWS_API_KEY = app_credentials.get(
                'NEWS_API_KEY') or ''
            DB_NAME = app_credentials.get(
                'DB_NAME') or ''
            DB_USERNAME = app_credentials.get(
                'DB_USERNAME') or ''
            DB_PASSWORD = app_credentials.get(
                'DB_PASSWORD') or ''
            DB_HOST = app_credentials.get(
                'DB_HOST') or ''
    else:
        print("app_credentials.json not found. "
              "Please create it and put your app credentials there.")

