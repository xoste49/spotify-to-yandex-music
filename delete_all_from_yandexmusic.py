"""
Скрипт удаляющий всё понравившуюся музыку из Яндекс.Музыка
"""

import os

from dotenv import load_dotenv
from progress.bar import Bar
from yandex_music import Client

load_dotenv()

client = Client(os.environ['YANDEX_MUSIC_TOKEN']).init()

print('Всего треков на удаление:', len(client.users_likes_tracks().tracks))
with Bar('Удаление', max=len(client.users_likes_tracks().tracks)) as bar:
    for track in client.users_likes_tracks().tracks:
        success = client.users_likes_tracks_remove(track.id)
        #answer = f'{track.id} Удален' if success else f'{track.id} Произошла ошибка'
        bar.next()

print('Осталось треков:', len(client.users_likes_tracks().tracks))
