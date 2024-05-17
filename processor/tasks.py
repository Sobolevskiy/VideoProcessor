import subprocess
import os

from celery import shared_task
from pytube import YouTube
from django.core.files import File
from django.utils.text import slugify

from processor.models import Video


@shared_task
def process_video(pk):
    video_instance = Video.objects.get(pk=pk)
    ffmpeg_command = ['ffmpeg', '-y', '-i', video_instance.file.path, '-f', 'null', '-']
    subprocess.run(ffmpeg_command)
    video_instance.processed = True
    video_instance.save()
    return video_instance.file.url


@shared_task
def download_youtube_video(url):
    video = Video.objects.create()
    yt = YouTube(url)
    stream = yt.streams.get_lowest_resolution()
    file_name = f'{slugify(yt.title)}.mp4'
    temp_file_path = f"/tmp/{file_name}"
    stream.download(output_path='/tmp', filename=file_name)

    with open(temp_file_path, 'rb') as f:
        video.file.save(file_name, File(f), save=True)

    os.remove(temp_file_path)

    return video.pk
