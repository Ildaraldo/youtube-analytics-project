import json
from googleapiclient.discovery import build
import os


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id  # id канала

        try:
            # объект для работы с API
            self.__youtube = self.get_service()

            # получение данных канала по его id
            self.__channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics,topicDetails').execute()

            # подтягиваем данные с API
            self.__title = self.__channel['items'][0]['snippet']['title']  # название канала
            self.__description = self.__channel['items'][0]['snippet']['description']  # описание канала
            self.__url = f"https://www.youtube.com/channel/{self.__channel['items'][0]['id']}"  # ссылка на канал
            self.__subscriber_count = self.__channel['items'][0]['statistics']['subscriberCount']  # количество подписчиков
            self.__video_count = self.__channel['items'][0]['statistics']['videoCount']  # количество видео
            self.__view_count = self.__channel['items'][0]['statistics']['viewCount']  # общее количество просмотров

            # данные по плейлистам канала
            self.__channel_playlists = self.__youtube.playlists().list(channelId=self.__channel_id,
                                                                       part='contentDetails,snippet',
                                                                       maxResults=50,
                                                                       ).execute()
        except Exception:
            # сообщение об ошибке
            print('Не удалось получить данные канала по его id')

            self.__youtube = None  # объект для работы с API
            self.__channel = None
            self.__title = None  # название канала
            self.__description = None  # описание канала
            self.__url = None  # ссылка на канал
            self.__subscriber_count = None  # количество подписчиков
            self.__video_count = None  # количество видео
            self.__view_count = None  # общее количество просмотров
            self.__channel_playlists = None  # данные по плейлистам канала

    def __str__(self):
        return f"'{self.__title} ({self.__url})'"
        # 'MoscowPython (https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A)'

    def __add__(self, other):
        return int(self.__subscriber_count) + int(other.__subscriber_count)

    def __sub__(self, other):
        return int(self.__subscriber_count) - int(other.__subscriber_count)

    def __gt__(self, other):
        return int(self.__subscriber_count) > int(other.__subscriber_count)

    def __ge__(self, other):
        return int(self.__subscriber_count) >= int(other.__subscriber_count)

    def __lt__(self, other):
        return int(self.__subscriber_count) < int(other.__subscriber_count)

    def __le__(self, other):
        return int(self.__subscriber_count) <= int(other.__subscriber_count)

    def __eq__(self, other):
        return int(self.__subscriber_count) == int(other.__subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def video_count(self):
        return self.__video_count

    @property
    def url(self):
        return self.__url

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f"id канала: '{self.__channel_id}'")
        # print(self.__channel)
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        # YT_API_KEY --> API-ключ
        api_key: str = os.getenv('YT_API_KEY')

        # объект для работы с API
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        """Метод, сохраняющий в файл значения атрибутов экземпляра Channel"""
        with open(filename, 'w') as file:
            file.write(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    def playlist(self, playlist_id):
        """Функция, возвращающая данные плейлиста канала по его id"""
        for item in self.__channel_playlists['items']:
            if item['id'] == playlist_id:
                return item

        return None
