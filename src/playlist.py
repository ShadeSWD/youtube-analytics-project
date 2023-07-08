import os
from datetime import timedelta
import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для ютуб-плейлиста"""
    api_key: str = str(os.getenv('API_KEY'))
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__playlist_id = playlist_id
        self.title: str = self.youtube.playlists().list(id=playlist_id, part='snippet,contentDetails',
                                                        maxResults=50).execute().get('items')[0].get('snippet').get(
            'title')
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

        self.__playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                   part='contentDetails',
                                                                   maxResults=50,
                                                                   ).execute()
        self.__video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]
        self.__video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                           id=','.join(self.__video_ids)
                                                           ).execute()

    def __str__(self):
        return f"{self.title}"

    @property
    def total_duration(self) -> timedelta:
        """datetime.timedelta: Геттер для суммарной длительности плейлиста."""
        total_duration = timedelta()
        for video in self.__video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).
        """
        best_video = max(self.__video_response.get('items'), key=lambda video: video['statistics']['likeCount'])
        video_id = best_video.get('id')
        return f'https://youtu.be/{video_id}'
