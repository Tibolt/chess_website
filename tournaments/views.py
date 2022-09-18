from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Bracket, Player
from .forms import BracketForm
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


def add_bracket(response):
    submitted = False
    if response.method == 'POST':
        form = BracketForm(response.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/brackets/add?submitted=True')
    else:
        form = BracketForm
        if 'submitted' in response.GET:
            submitted = True
    context = {'form': form, 'submitted': submitted}
    return render(response, 'tournaments/add_bracket.html', context)
