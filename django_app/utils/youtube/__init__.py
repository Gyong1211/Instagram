import requests
from googleapiclient.discovery import build


def search_original(q):
    url_youtube_search = 'https://www.googleapis.com/youtube/v3/search'
    YOUTUBE_API_ACCESS_TOKEN = 'AIzaSyD3CQXSZwqDBN8uHbfmiB8KazDBb2bwEX0'
    url_youtube_search_params = {
        'part': 'snippet',
        'key': YOUTUBE_API_ACCESS_TOKEN,
        'q': q,
        'maxResults': 5,
        'type': 'video'
    }
    response = requests.get(url_youtube_search, params=url_youtube_search_params)
    data = response.json()
    return data


def search(q):
    DEVELOPER_KEY = 'AIzaSyD3CQXSZwqDBN8uHbfmiB8KazDBb2bwEX0'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=q,
        part='snippet',
        maxResults=5,
        type='video',
    ).execute()
    return search_response

