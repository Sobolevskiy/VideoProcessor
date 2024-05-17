from django.urls import path

from processor.views import home, upload_video, get_task_status, upload_youtube

urlpatterns = [
    path("", home, name="home"),
    path("upload_video/", upload_video, name="upload_video"),
    path("get_task_status/<str:task_id>/", get_task_status, name="get_task_status"),
    path("upload_youtube/", upload_youtube, name="upload_youtube")
]