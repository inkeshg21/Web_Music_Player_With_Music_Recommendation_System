from django.shortcuts import render

from account.auth import user_only
from music.models import Music


# Create your views here.
@user_only
def index(request):
    musics = Music.objects.all()
    context = {
        'musics': musics,
        'active_home': 'badge-primary text-primary rounded'
    }
    return render(request, 'music/index.html', context)
