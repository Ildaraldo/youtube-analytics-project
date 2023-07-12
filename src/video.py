from datetime import datetime, timedelta
from src.channel import Channel
import json
import isodate


class Video(Channel):
    """Класс для видео ютуб-канала"""

    def __init__(self, video_id: str) -> None:
        # получение данных видео по его id
        self.__video = self.__class__.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                  id=video_id
                                                                  ).execute()

        # инициализация класса 'Channel'
        super().__init__(self.__video['items'][0]['snippet']['channelId'])

        self.__video_id = video_id  # id видео
        self.__title = self.__video['items'][0]['snippet']['title']  # название видео
        self.__url = f"https://youtu.be/{self.__video_id}"  # ссылка на видео
        self.__view_count = self.__video['items'][0]['statistics']['viewCount']  # количество просмотров
        self.__like_count = self.__video['items'][0]['statistics']['likeCount']  # количество лайков

        # длительность видео
        self.__duration = timedelta(
            seconds=isodate.parse_duration(self.__video['items'][0]['contentDetails']['duration']).total_seconds())

    def __str__(self):
        return f"{self.__title}"

    @property
    def video_id(self):
        return self.__video_id

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count

    @property
    def duration(self) -> timedelta:
        return self.__duration

    def to_json(self, filename):
        """Метод, сохраняющий в файл значения атрибутов экземпляра Video"""
        with open(filename, 'w') as file:
            file.write(json.dumps(self.video_id, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f"id канала: '{self.__video_id}'")
        # print(self.__video)
        print(json.dumps(self.__video, indent=2, ensure_ascii=False))


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        # id плей-листа
        self.__playlist_id = playlist_id

        # получение данных плей-листа по его id
        self.__playlist = super().get_service().playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()

        # получение списка id видео
        self.__playlist_videos_id = [item["contentDetails"]["videoId"] for item in self.__playlist["items"]]

        if video_id in self.__playlist_videos_id:
            super().__init__(video_id)
        else:
            raise Exception(f"В плей-листе c id '{self.__playlist_id}' отсутствует видео с id {video_id}")
