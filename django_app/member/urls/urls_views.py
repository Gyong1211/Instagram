from django.conf.urls import url

from .. import views

app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^login/facebook$', views.facebook_login, name='facebook_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='my_profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^profile/(?P<user_pk>\d+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<user_pk>\d+)/follow_toggle/$', views.follow_toggle, name='follow_toggle'),
    url(r'^profile/(?P<user_pk>\d+)/block_toggle/$', views.block_toggle, name='block_toggle'),
]
