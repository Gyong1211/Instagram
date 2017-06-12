from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^(?P<post_pk>\d+)/detail/$', views.post_list),
    url(r'^$', views.post_list),
    url(r'^$', views.post_list),
]
