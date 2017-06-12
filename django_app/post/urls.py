from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^(?P<post_pk>\d+)/$', views.post_detail),
    url(r'^$', views.post_list),
    url(r'^$', views.post_list),
]
