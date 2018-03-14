from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    # url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', login_required(views.post_new), name='post_new'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^home/$', views.home, name='home'),
]