from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

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


def play_music(request, id):
    music = Music.objects.get(id=id)
    context = {
        "music": music
    }

    html = render_to_string('player.html', context)

    return JsonResponse({"success": True, "data": html})