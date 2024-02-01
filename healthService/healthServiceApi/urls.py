from django.urls import path
from .views import ping, submit_server_or_check_server, check_all_servers, ready, start
urlpatterns = [
    path("ping/", ping),
    path("server/", submit_server_or_check_server),
    path("server/all/", check_all_servers),
    path("ready/", ready),
    path("start/", start)
]
