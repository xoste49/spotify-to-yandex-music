"""
Скрипт удаляющий всё понравившуюся музыку из Яндекс.Музыка
"""

import os
from pprint import pprint

from yandex_music import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.environ['YANDEX_MUSIC_TOKEN']).init()

print('Всего треков на удаление:', len(client.users_likes_tracks().tracks))
for track in client.users_likes_tracks().tracks:
    success = client.users_likes_tracks_remove(track.id)
    answer = f'{track.id} Удален' if success else f'{track.id} Произошла ошибка'
    print(answer)

print('Осталось треков:', len(client.users_likes_tracks().tracks))
