from src.base_youtube_service import BaseYouTubeService


class Video(BaseYouTubeService):
    """Класс для ютуб-видео"""
    base_url = f'https://www.youtube.com/watch?v='

    def __init__(self, video_id) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        super().__init__()
        self.__video_id = video_id
        try:
            video_response = self.youtube.videos().list(id=self.__video_id, part='snippet,statistics').execute()
            self.title: str = video_response['items'][0]['snippet']['title']
            self.url = f'{self.base_url}{self.__video_id}'
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    """Класс для ютуб-видео в плейлисте"""
    def __init__(self, video_id, playlist_id) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)
        self.playlist_id = playlist_id
