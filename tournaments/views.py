from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import permission_required

from .models import Bracket, Player, Rounds
from .forms import BracketForm, PlayersForm

# Create your views here.


def index(response):
    return render(response, 'tournaments/index.html', {})


def brackets_list(response):
    brackets = Bracket.objects.all()
    size = []
    for x in brackets:
        size.append(Player.objects.filter(bracket=x).count())

    br = zip(brackets, size)
    return render(response, 'tournaments/brackets_list.html', {'brackets': br})


def bracket(response, id):
    bracket = get_object_or_404(Bracket, pk=id)
    players = Player.objects.filter(bracket=id).all()

    response.session['sorting'] = ""
    # persist sorting session variable
    if response.GET.get('sort'):
        response.session['sorting'] = response.GET.get('sort')
    else:
        response.session['sorting']
    field_names = [f.name for f in Player._meta.get_fields()]
    field_names_desc = ['-' + f.name for f in Player._meta.get_fields()]

    match response.session['sorting']:
        case x:
            if x in field_names:
                players = players.order_by(str(x))
            elif x in field_names_desc:
                players = players.order_by(str(x))
            else:
                players = players.order_by('pk')
    context = {
        'bracket': bracket,
        'players': players,
        'response': response,
    }
    return render(response, 'tournaments/bracket.html', context)

@permission_required('tournaments.moderator')
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


@permission_required('tournaments.moderator')
def add_players(response, id):
    bracket = Bracket.objects.get(pk=id)
    if response.method == "POST":
        form = PlayersForm(response.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.bracket = bracket
            form.save()
            return HttpResponseRedirect('/brackets/table/' + str(id))

    else:
        form = PlayersForm()
    context = {'form': form}
    return render(response, 'tournaments/add_players.html', context)


@permission_required('tournaments.moderator')
def edit_players(response, id):
    bracket = Bracket.objects.get(pk=id)
    PlayerInlineFormSet = inlineformset_factory(
        Bracket, Player, fields=['name', 'last_name', 'age', 'rating', 'score'])
    if response.method == 'POST':
        formset = PlayerInlineFormSet(response.POST, response.FILES, instance=bracket)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/brackets/table/' + str(id))
    else:
        formset = PlayerInlineFormSet(instance=bracket)
    context = {'form': formset}
    return render(response, 'tournaments/edit_players.html', context)


def rounds(response, id, round):
    bracket = get_object_or_404(Bracket, pk=id)
    players = Player.objects.filter(bracket=id).all()
    rounds = Rounds.objects.filter(bracket=id).filter(round=round).all()
    
    if rounds.exists():
        first_half = Player.objects.filter(id__in=rounds.values('player1_id')).order_by("-rating")
        second_half = Player.objects.filter(id__in=rounds.values('player2_id')).order_by("-rating")

    else:
        if round > 0:
            first_half = players.order_by("-score")[:len(players) / 2]
            second_half = players.order_by("-score")[len(players) / 2:len(players)]
        else:
            first_half = players.order_by("-rating")[:len(players) / 2]
            second_half = players.order_by("-rating")[len(players) / 2:len(players)]

        match_history = {}
        # save history to db
        if response.method == 'POST':
            for index, p1 in enumerate(first_half):
                match_history[p1] = second_half[index]
                rd, new_rd = Rounds.objects.update_or_create(bracket=bracket, round=round,
                                           player1_id=p1.pk, player2_id=second_half[index].pk, player1_score=p1.score_round, player2_score=second_half[index].score_round)
                rd.save()
            return HttpResponseRedirect('/brackets/table/' + str(id) + "/rounds/" + str(round))

    context = {
        'first_half': first_half,
        'second_half': second_half,
        'bracket': bracket,
        'rd': str(round),
    }
    return render(response, 'tournaments/rounds.html', context)


@permission_required('tournaments.moderator')
def edit_rounds(response, id, round):
    bracket = get_object_or_404(Bracket, pk=id)
    rounds = Rounds.objects.filter(bracket=bracket).filter(round=round).all()
    players1 = Player.objects.filter(id__in=rounds.values('player1_id')).order_by("-rating")
    players2 = Player.objects.filter(id__in=rounds.values('player2_id')).order_by("-rating")

    # if round > 0:
    #     players1 = players1.order_by("-score", "rating")
    #     players2 = players2.order_by("-score", "rating")
    # else:
    #     players1 = players1.order_by("-rating")
    #     players2 = players2.order_by("-rating")

    if response.method == 'POST':
        for player in players1:
            if(response.POST.get("p1" + str(player.pk))) != '':
                rounds.filter(player1_id=player.pk).update(player1_score=int(response.POST.get("p1" + str(player.pk))))
                player.score = rounds.filter(player1_id=player.pk).aggregate(Sum('player1_score'))['player1_score__sum']
                player.score_round = 0
                # player.score += int(response.POST.get("p1" + str(player.pk)))
                player.score_round = int(response.POST.get("p1" + str(player.pk)))
                player.save()

        for player in players2:
            if(response.POST.get("p2" + str(player.pk))) != '':
                rounds.filter(player2_id=player.pk).update(player2_score=int(response.POST.get("p2" + str(player.pk))))
                player.score = rounds.filter(player2_id=player.pk).aggregate(Sum('player2_score'))['player2_score__sum']
                player.score_round = 0
                # player.score += int(response.POST.get("p2" + str(player.pk)))
                player.score_round = int(response.POST.get("p2" + str(player.pk)))
                player.save()
        return HttpResponseRedirect('/brackets/table/' + str(id) + "/rounds/" + str(round))

    context = {
        'rounds': rounds,
        'bracket': bracket,
        'rd': round,
        'players1': players1,
        'players2': players2,
    }
    return render(response, 'tournaments/edit_rounds.html', context)
