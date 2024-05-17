from django.shortcuts import render, redirect
from django.http import JsonResponse
from celery import chain
from celery.result import AsyncResult

from processor.forms import UploadForm, YouTubeURLForm
from processor.tasks import process_video, download_youtube_video


def home(request):
    context = {
        'form': UploadForm(),
        'you_tube_form': YouTubeURLForm(),
    }
    return render(request, 'home.html', context)


def video_processing(func):
    def wrapper(request, *args, **kwargs):
        context = dict()
        if request.method == 'POST':
            context['task_id'] = func(request, *args, **kwargs)
            return render(request, 'process.html', context=context)
        return JsonResponse({'msg': 'GET not supported'}, status=405)

    return wrapper


@video_processing
def upload_video(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        uploaded_video = form.save()
        task_result = process_video.apply_async(args=[uploaded_video.pk])
        return task_result.id
    return None


@video_processing
def upload_youtube(request):
    form = YouTubeURLForm(request.POST)
    if form.is_valid():
        task_result = chain(download_youtube_video.s(form.cleaned_data['youtube_url']), process_video.s())()
        return task_result.id
    return None


def get_task_status(request, task_id):
    task_result = AsyncResult(task_id)

    response = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.get() if task_result.status == 'SUCCESS' else None,
    }
    return JsonResponse(response)
