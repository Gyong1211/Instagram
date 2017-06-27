import requests
from django.shortcuts import render

__all__ = (
    'youtube_search',
)


def youtube_search(request):
    url_youtube_search = 'https://www.googleapis.com/youtube/v3/search'
    YOUTUBE_API_ACCESS_TOKEN = 'AIzaSyAUvTn6g5D6DmX6dHk4_LfNY3rzH1wqRxA'
    print(request.GET)
    q = request.GET.get('q')
    if q:
        url_youtube_search_params = {
            'part': 'snippet',
            'key': YOUTUBE_API_ACCESS_TOKEN,
            'q': q,
            'maxResults': 5,
            'type': 'video'
        }
        response = requests.get(url_youtube_search, params=url_youtube_search_params)
        context = {
            'response': response.json(),
        }
        return render(request, 'post/youtube_search.html', context=context)

    return render(request, 'post/youtube_search.html')
