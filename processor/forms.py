from django import forms

from processor.models import Video


class UploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file',]


class YouTubeURLForm(forms.Form):
    youtube_url = forms.URLField(label='YouTube URL')
