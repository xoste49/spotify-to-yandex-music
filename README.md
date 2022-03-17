# Spotify To Yandex.Music
Из-за возможной блокировкой Spotify написал пару скриптов для копирования музыки из Spotify в Яндекс.Музыка

[Способ получения токена Яндекс.Музыки.](https://github.com/xoste49/yandex-music-token)  
[Получить SPOTIPY_CLIENT_ID и SPOTIPY_CLIENT_SECRET.](https://developer.spotify.com/dashboard/applications)
(В настройках созданного приложения нужно указать 'Redirect URIs', туда вводим 'http://localhost:8080')

## Environments
```sh
SPOTIPY_CLIENT_ID= Client ID вашего приложения
SPOTIPY_CLIENT_SECRET= Client Secret вашего приложения
SPOTIPY_REDIRECT_URI=http://localhost:8080
YANDEX_MUSIC_TOKEN=Тут токен от Яндекс.Музыка
```
вот мои SPOTIPY_CLIENT_ID и SPOTIPY_CLIENT_SECRET если лень создавать приложение
```sh
SPOTIPY_CLIENT_ID=6f2c8bcbfd7e436cb5faeaad03cd64f8
SPOTIPY_CLIENT_SECRET=837df16128e64f8cbaab2c0de2ceaaf1
```

## Как работает
```bash
git clone https://github.com/xoste49/spotify-to-yandex-music.git
cd spotify-to-yandex-music
touch .env
nano .env # Environments
pip install -r requirements.txt
python transfer.py
```

## Удаление всех треков из плейлиста "Мне нравится" на Яндекс.Музыка
```bash
pip install -r requirements.txt
python delete_all_from_yandexmusic.py
```

## Скриншоты

![screenshot](https://user-images.githubusercontent.com/7299412/158782647-a1392ad6-2854-40d6-acb9-2213012bef3a.png)

## Используемые библиотеки
spotipy: https://github.com/plamere/spotipy  
yandex-music: https://github.com/MarshalX/yandex-music-api  
progress: https://github.com/verigak/progress/  
