from django.db import models

__all__ = (
    'Video',
)


class VideoManager(models.Manager):
    def created_from_search_result(self, result):
        youtube_id = result['id']['videoId']
        title = result['snippet']['title']
        description = result['snippet']['description']
        thumbnail = result['snippet']['thumbnails']['high']['url']

        video, video_created = Video.objects.get_or_create(
            youtube_id=youtube_id,
            defaults={
                'title': title,
                'description': description,
                'url_thumbnail': thumbnail,
            }
        )
        print('Video({})is {}'.format(
            video.title,
            'created' if video_created else 'already exists',
        ))
        return video


class Video(models.Model):
    youtube_id = models.CharField(
        max_length=50,
        unique=True,
    )
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField(blank=True)
    url_thumbnail = models.CharField(
        max_length=200,
    )

    objects = VideoManager()

    def __str__(self):
        return self.title
