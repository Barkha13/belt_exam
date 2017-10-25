from django.conf.urls import url
from . import views 
urlpatterns = [
    url(r'^$',views.index),
    url(r'^process$',views.process),
    url(r'^login_process$',views.login_process),
    url(r'^quotes$',views.quotes),
    url(r'^quotes/add_quote$',views.add_quote),
    url(r'^quotes/(?P<id>\d+)$',views.add_favorite),
    url(r'^quotes/remove/(?P<id>\d+)$',views.remove_favorite),
    url(r'^users/(?P<id>\d+)$',views.show_user)

]