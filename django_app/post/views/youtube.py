import requests
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ..models import Video, Post, Comment

__all__ = (
    'youtube_search',
    'post_create_with_video'
)


def youtube_search(request):
    url_youtube_search = 'https://www.googleapis.com/youtube/v3/search'
    YOUTUBE_API_ACCESS_TOKEN = 'AIzaSyAUvTn6g5D6DmX6dHk4_LfNY3rzH1wqRxA'
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
        data = response.json()
        for item in data['items']:
            Video.objects.created_from_search_result(item)

        # videos = Video.objects.filter(title__contains=q)  # 제목에 검색어가 포함되는 경우
        # videos = Video.objects.filter(Q(title__contains=q) | Q(description__contains=q)) # 제목과 설명에 검색어가 포함되는 경우

        # videos = Video.objects.all() # 검색어가 띄워쓰기로 구분되어 있는 경우 모든 검색어를 포함하는 경우(and) / 원초적인 방법
        # for cur_q in q.split(' '):
        #     videos.filter(title__contains=cur_q)
        # videos.filter(title__contains=검색어1).filter(title__contains=검색어2).filter(title__contains=검색어3)....

        # 검색어가 띄워쓰기로 구분되어 있는 경우 모든 검색어를 포함하는 경우(and) / regex 사용
        re_pattern = ''.join(['(?=.*{})'.format(item) for item in q.split()])
        # re_pattern = (?=.*검색어1)(?=.*검색어2)(?=.*검색어3)...
        videos = Video.objects.filter(title__regex='{}'.format(re_pattern))

        # # 검색어가 띄워쓰기로 구분되어 있는 경우 검색어중 하나라도 포함하는 경우(or) / regex 사용
        # re_pattern = '|'.join(['({})'.format(item) for item in q.split()])
        # # re_pattern = (검색어1)|(검색어2)|(검색어3)...
        # videos = Video.objects.filter(title__regex='{}'.format(re_pattern))

        context = {
            'videos': videos
        }

        return render(request, 'post/youtube_search.html', context=context)

    return render(request, 'post/youtube_search.html')


@require_POST
@login_required
def post_create_with_video(request):
    video_pk = request.POST['video_pk']
    video = get_object_or_404(Video, pk=video_pk)

    post = Post.objects.create(
        author=request.user,
        video=video,
    )
    post.my_comment = Comment.objects.create(
        author=request.user,
        post=post,
        content=video.title
    )
    return redirect('post:post_detail', post_pk=post.pk)
