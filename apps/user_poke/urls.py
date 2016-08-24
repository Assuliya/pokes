from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'user/(?P<user_id>\d+)$', views.user_page, name='user_page'),
    url(r'^user/login_process$', views.login_process, name='login_process'),
    url(r'^user/register_process$', views.register_process, name='register_process'),
    url(r'^user/logout$', views.logout, name='logout'),
    url(r'^user/(?P<user_id>\d+)/poke$', views.poke, name='poke')

]
