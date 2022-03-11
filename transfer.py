"""
Скрипт копирующий музыку из Spotify в Яндекс.Музыка
"""
import os
import time

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


not_add_tracks = []


def send_search_request_and_print_result(client, track, number, count_tracks):
    query = track['artist'] + ' - ' + track['name']
    search_result = client.search(query)

    text = [f'Результаты по запросу "{query}":', '']

    if len(query) < 70:
        query = "%70s" % query

    if search_result.best:
        type_ = search_result.best.type
        best = search_result.best.result

        if type_ in ['track', 'podcast_episode']:
            artists = ''
            if best.artists:
                artists = ', '.join(
                    artist.name for artist in best.artists) + ' - '
            if track['name'] in best.title:
                success = client.users_likes_tracks_add(best.id)
                if success:
                    return "✅ (%s/%s) %s | %s" % (
                    number, count_tracks, query, artists + best.title)
                else:
                    not_add_tracks.append("❌ %s | Произошла ошибка" % query)
                    return "❌ (%s/%s) %s | Произошла ошибка" % (
                    number, count_tracks, query)
    not_add_tracks.append("❌ %s | Трек не найден" % query)
    return "❌ (%s/%s) %s | Трек не найден" % (number, count_tracks, query)


if __name__ == '__main__':
    time_start_program = time.monotonic()
    Client()
    spotify_tracks = parse_spotify()
    spotify_tracks.reverse()

    client = Client(os.environ['YANDEX_MUSIC_TOKEN']).init()
    count_likes_tracks_before = len(client.users_likes_tracks().tracks)
    count_spotify_tracks = len(spotify_tracks)
    for number, track in enumerate(spotify_tracks):
        print(send_search_request_and_print_result(client, track, number,
                                             count_spotify_tracks))
    count_likes_tracks_after = len(client.users_likes_tracks().tracks)
    print('Количество добавленных треков:',
          (count_likes_tracks_after - count_likes_tracks_before))
    print('\nСписок не добавленых треков')
    for track in not_add_tracks:
        print(track)
    time_stop_program = time.monotonic()
    time_run_program = time_stop_program - time_start_program
    print('Время работы программы:', time_run_program)
