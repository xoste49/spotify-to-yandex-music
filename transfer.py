"""
Скрипт копирующий музыку из Spotify в Яндекс.Музыка
"""
import os
import sys
import urllib
from pprint import pprint

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from yandex_music import Client

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
    return tracks


not_add_tracks = []


def send_search_request_and_print_result(client, track, number, count_tracks):
    query = track['artist'] + ' - ' + track['name']
    search_result = client.search(query)

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
            if track['name'].casefold() in best.title.casefold():
                success = client.users_likes_tracks_add(best.id)
                if success:
                    return "✅ (%s/%s) %s | %s" % (
                    number, count_tracks, query, artists + best.title)
                else:
                    not_add_tracks.append(track['artist'] + ' - ' + track['name'])
                    return "❌ (%s/%s) %s | Произошла ошибка" % (
                    number, count_tracks, query)
            elif best.title.casefold() in track['name'].casefold():
                success = client.users_likes_tracks_add(best.id)
                if success:
                    return "✅ (%s/%s) %s | %s" % (
                        number, count_tracks, query, artists + best.title)
                else:
                    not_add_tracks.append(track['artist'] + ' - ' + track['name'])
                    return "❌ (%s/%s) %s | Произошла ошибка" % (
                    number, count_tracks, query)
    not_add_tracks.append(track['artist'] + ' - ' + track['name'])
    return "❌ (%s/%s) %s | Трек не найден" % (number, count_tracks, query)


def main(track_start_from=0):
    spotify_tracks = parse_spotify()
    spotify_tracks.reverse()

    client = Client(os.environ['YANDEX_MUSIC_TOKEN']).init()
    yandex_tracks = client.users_likes_tracks().tracks

    count_spotify_tracks = len(spotify_tracks)
    print('Всего треков в spotify', count_spotify_tracks, '\n')

    count_likes_tracks_before = len(yandex_tracks)
    for number, track in enumerate(spotify_tracks):
        if number >= track_start_from:
            print(send_search_request_and_print_result(
                client, track, number, count_spotify_tracks
            ))
    count_likes_tracks_after = len(client.users_likes_tracks().tracks)
    print('Количество добавленных треков:',
          (count_likes_tracks_after - count_likes_tracks_before))
    print('\nСписок не добавленых треков:', len(not_add_tracks))
    for track in not_add_tracks:
        print('❌ %s | https://music.yandex.ru/search?text=%s&type=tracks' %
              (track, urllib.parse.quote(track)))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main(0)
    else:
        if len(sys.argv) < 3:
            print("Ошибка. Слишком мало параметров.")
            sys.exit(1)

        if len(sys.argv) > 3:
            print("Ошибка. Слишком много параметров.")
            sys.exit(1)

        param_name = sys.argv[1]
        param_value = sys.argv[2]

        if (param_name == "--from" or
                param_name == "-f"):
            try:
                type(int(param_value))
            except ValueError:
                print(f'В {param_name} должно передаваться число!')
                sys.exit(1)
            main(int(param_value))
        else:
            print("Ошибка. Неизвестный параметр '{}'".format(param_name))
            sys.exit(1)
