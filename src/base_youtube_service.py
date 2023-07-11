from googleapiclient.discovery import build
import os


class BaseYouTubeService:
    base_url = ''
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
