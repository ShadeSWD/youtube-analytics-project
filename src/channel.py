import json
from src.base_youtube_service import BaseYouTubeService


class Channel(BaseYouTubeService):
    """Класс для ютуб-канала"""
    base_url = r'https://www.youtube.com/channel/'

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        super().__init__()
        self.__channel_id = channel_id
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f'{self.base_url}{self.__channel_id}'
        self.subscriber_count = int(channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(channel["items"][0]["statistics"]["videoCount"])
        self.view_count = int(channel["items"][0]["statistics"]["viewCount"])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        if self.subscriber_count < other.subscriber_count:
            return True
        else:
            return False

    def __le__(self, other):
        if self.subscriber_count <= other.subscriber_count:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.subscriber_count > other.subscriber_count:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.subscriber_count >= other.subscriber_count:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.subscriber_count == other.subscriber_count:
            return True
        else:
            return False

    def to_json(self, filename):
        """
        Saves channel's attributes to .json file
        """
        with open(f'{filename}', 'w') as file:
            channel = {
                "__channel_id": self.__channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscriber_count": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count
            }
            json.dump(channel, file, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.printj(channel)

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
