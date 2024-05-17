from django.contrib import admin

from processor.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'processed')
    list_filter = ('processed',)
