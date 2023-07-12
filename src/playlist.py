import json
from datetime import timedelta
from src.channel import Channel
from src.video import Video


class PlayList(Channel):
    def __init__(self, playlist_id: str):
        self.__playlist_id = playlist_id

        # получение данных плей-листа по его id
        self.__playlist = self.__class__.get_service().playlistItems().list(playlistId=playlist_id,
                                                                            part='contentDetails,snippet',
                                                                            maxResults=50,
                                                                            ).execute()

        # инициализация класса 'Channel'
        super().__init__(self.__playlist['items'][0]['snippet']['channelId'])

        # название плей-листа
        self.__title = super().playlist(playlist_id)['snippet']['title']

        # ссылка на плейлист
        self.__url = f'https://www.youtube.com/playlist?list={playlist_id}'

        # получение списка id видео
        self.__id_videos = [item['contentDetails']['videoId'] for item in self.__playlist['items']]

        # список видео плейлиста
        self.__videos = [Video(id_video) for id_video in self.__id_videos]

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    def total_duration(self):
        """Функция, возвращающая суммарную длительность плейлиста"""
        total_time = timedelta()
        for video in self.__videos:
            total_time += video.duration

        return total_time

    def show_best_video(self):
        """Функция, возвращающая ссылку на видео с максимальным количеством лайков"""
        index = 0
        for i in range(0, len(self.__videos)):
            if self.__videos[index].like_count < self.__videos[i].like_count:
                index = i

        return self.__videos[index].url

    def print_info(self) -> None:
        """Выводит в консоль информацию о плей-листе."""
        print(f"id плей-листа: '{self.__playlist_id}'")
        # print(self.__channel)
        print(json.dumps(self.__playlist, indent=2, ensure_ascii=False))



