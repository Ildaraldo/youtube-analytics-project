from src.channel import Channel

if __name__ == '__main__':
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')

    # получаем значения атрибутов
    print(moscowpython.title)  # MoscowPython
    print(moscowpython.video_count)  # 685 (может уже больше)
    print(f"{moscowpython.url} \n")  # https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A

    try:
        # менять не можем
        moscowpython.channel_id = 'Новое название'
    except AttributeError:
        # AttributeError: property 'channel_id' of 'Channel' object has no setter
        print('Нельзя менять "channel_id" т.к. не задан setter')

    # можем получить объект для работы с API вне класса
    print(f"\n{Channel.get_service()}")
    # <googleapiclient.discovery.Resource object at 0x000002B1E54F9750>

    # создаем файл 'moscowpython.json' в данными по каналу
    moscowpython.to_json('moscowpython.json')
