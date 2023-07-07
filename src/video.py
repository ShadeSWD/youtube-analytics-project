import os
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-видео"""
    api_key: str = str(os.getenv('API_KEY'))
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        video_response = self.youtube.videos().list(id=self.__video_id, part='snippet,statistics').execute()
        self.title: str = video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.__video_id}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    """Класс для ютуб-видео в плейлисте"""
    def __init__(self, video_id, playlist_id) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)
        self.playlist_id = playlist_id
