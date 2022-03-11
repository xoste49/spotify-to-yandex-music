"""
Скрипт копирующий музыку из Spotify в Яндекс.Музыка
"""
import os
from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from yandex_music import Client

from dotenv import load_dotenv

load_dotenv()


def parse_spotify():
    tracks = []

    def add_tracks_list(results):
        for item in results['items']:
            track = item['track']
            tracks.append(
                {'artist': track['artists'][0]['name'], 'name': track['name']})

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

    results = sp.current_user_saved_tracks()
    add_tracks_list(results)

    while results['next']:
        results = sp.next(results)
        add_tracks_list(results)

    print('Всего треков в spotify', len(tracks), '\n')
    return tracks


type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}

count_transferred_tracks = 0


def send_search_request_and_print_result(client, track):
    query = track['artist'] + ' - ' + track['name']
    search_result = client.search(query)

    text = [f'Результаты по запросу "{query}":', '']

    if len(query) < 75:
        query = "%75s" % query

    if search_result.best:
        type_ = search_result.best.type
        best = search_result.best.result

        text.append(f'❗️Лучший результат: {type_to_name.get(type_)}')

        if type_ in ['track', 'podcast_episode']:
            artists = ''
            if best.artists:
                artists = ', '.join(
                    artist.name for artist in best.artists) + ' - '
            if track['name'] in best.title:
                success = client.users_likes_tracks_add(best.id)
                if success:
                    print("✅ %s | %s" % (query, artists + best.title))
                else:
                    print("❌ %s | Произошла ошибка" % query)
            else:
                print("❌ %s | Трек не найден" % query)
        else:
            print("❌ %s | Трек не найден" % query)
    else:
        print("❌ %s | Трек не найден" % query)


if __name__ == '__main__':
    Client()
    spotify_tracks = parse_spotify()
    spotify_tracks.reverse()

    client = Client(os.environ['YANDEX_MUSIC_TOKEN']).init()
    count_likes_tracks_before = len(client.users_likes_tracks().tracks)
    for track in spotify_tracks:
        send_search_request_and_print_result(client, track)
    count_likes_tracks_after = len(client.users_likes_tracks().tracks)
    print('Количество добавленных треков:',
          (count_likes_tracks_after-count_likes_tracks_before))
