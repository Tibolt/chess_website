from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Bracket, Player
# Create your views here.


def index(response):
    return render(response, 'tournaments/index.html', {})


def brackets_list(response):
    brackets = Bracket.objects.all()
    return render(response, 'tournaments/brackets_list.html', {'brackets': brackets})


def bracket(response, id):
    bracket = get_object_or_404(Bracket, pk=id)
    players = Player.objects.filter(bracket=id).all()
    context = {
        'bracket': bracket,
        'players': players,
    }
    return render(response, 'tournaments/bracket.html', context)

