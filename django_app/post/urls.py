from django.conf.urls import url

from post import views

app_name = 'post'
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<post_pk>\d+)/modify/$', views.post_modify, name='post_modify'),
    url(r'^(?P<post_pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^(?P<post_pk>\d+)/comment_create/$',views.comment_create, name='comment_create'),
    url(r'^(?P<post_pk>\d+)/comment_modify/(?P<comment_pk>\d+)/$', views.comment_modify, name='comment_modify'),
    url(r'^(?P<post_pk>\d+)/comment_delete/(?P<comment_pk>\d+)/$', views.comment_delete, name='comment_delete'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.hashtag_post_list, name='hashtag_post_list'),
    url(r'^(?P<post_pk>\d+)/like/$', views.post_like, name='post_like'),
]
