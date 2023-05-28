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

    refresh_score(id)

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
            bracket_id = Bracket.objects.latest('id').id
            nuber_of_rounds = Bracket.objects.latest('id').numberOfRounds
            create_rounds(bracket_id, nuber_of_rounds)
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

    refresh_round_score(id, round)

    # # if round in rounds table get score from rounds table for each half of players and sort them by rating if round is 0 or score if round is > 0
    if round > 1:
        first_half = players.filter(id__in=rounds.values('player1_id'))
        second_half = players.filter(id__in=rounds.values('player2_id'))
    else:
        players = players.order_by("-rating")
        first_half = players[:len(players)//2]
        second_half = players[len(players)//2:]

    
    # first_half, second_half = sort_players(id, round)


    context = {
        'first_half': first_half,
        'second_half': second_half,
        'bracket': bracket,
        'rd': str(round),
        'rounds_number': range(1,bracket.numberOfRounds+1)
    }
    return render(response, 'tournaments/rounds.html', context)


@permission_required('tournaments.moderator')
def edit_rounds(response, id, round):
    bracket = get_object_or_404(Bracket, pk=id)
    rounds = Rounds.objects.filter(bracket=bracket).filter(round=round).all()


    # create_rounds(id, bracket.numberOfRounds)
    first_half, second_half = sort_players(id, round)
    for p1, p2 in zip(first_half, second_half):
        create_round_and_add_players(id, round, p1.id, p2.id)

    players1 = Player.objects.filter(id__in=rounds.values('player1_id')).order_by("-rating")
    players2 = Player.objects.filter(id__in=rounds.values('player2_id')).order_by("-rating")

    

    if response.method == 'POST':
        for player in players1:
            if(response.POST.get("p1" + str(player.pk))) != '':
                rounds.filter(player1_id=player.pk).update(player1_score=int(response.POST.get("p1" + str(player.pk))))
                player.score = rounds.filter(player1_id=player.pk).aggregate(Sum('player1_score'))['player1_score__sum']
                player.score_round = rounds.filter(player1_id=player.pk).get().player1_score
                player.save()

        for player in players2:
            if(response.POST.get("p2" + str(player.pk))) != '':
                rounds.filter(player2_id=player.pk).update(player2_score=int(response.POST.get("p2" + str(player.pk))))
                player.score = rounds.filter(player2_id=player.pk).aggregate(Sum('player2_score'))['player2_score__sum']
                player.score_round = rounds.filter(player2_id=player.pk).get().player2_score
                player.save()

        # if round is mark as Finished call add_players_to_round function
        if response.POST.get("finished") == 'on':
            print("finised")
            # set round as finished
            rd = Rounds.objects.filter(bracket=bracket).filter(round=round)
            print(rd)
            for r in rd:
                print(r.id, r.isFinished)
                r.isFinished = True
                print(r.id, r.isFinished)
                r.save()
            if round+1 in rounds.values('round') and rounds.last().isFinished == True:
                print("debug add players")
                # add_players_to_round(id, round+1)

        return HttpResponseRedirect('/brackets/table/' + str(id) + "/rounds/" + str(round))

    context = {
        'rounds': rounds,
        'bracket': bracket,
        'rd': round,
        'players1': players1,
        'players2': players2,
    }
    return render(response, 'tournaments/edit_rounds.html', context)


@permission_required('tournaments.moderator')
def add_round(response, id, round):
    bracket = get_object_or_404(Bracket, pk=id)
    
    bracket.numberOfRounds = bracket.numberOfRounds + 1
    bracket.save(update_fields=['numberOfRounds'])

    return rounds(response, id, round)

def refresh_round_score(bracket_id, round_id):
    bracket = get_object_or_404(Bracket, pk=bracket_id)
    round = Rounds.objects.filter(bracket=bracket).filter(round=round_id).all()
    players = Player.objects.filter(bracket=bracket).all()
    for player in players:
        s1, s2 = 0, 0
        if round.filter(player1_id=player.pk).first() is not None:
            s1 = round.filter(player1_id=player.pk).first().player1_score or 0
        if round.filter(player2_id=player.pk).first() is not None:
            s2 = round.filter(player2_id=player.pk).first().player2_score or 0
        player.score_round = s1 + s2
        player.save()


def refresh_score(bracket_id):
    bracket = get_object_or_404(Bracket, pk=bracket_id)
    rounds = Rounds.objects.filter(bracket=bracket).all()
    players = Player.objects.filter(bracket=bracket).all()
    for player in players:
        s1 = rounds.filter(player1_id=player.pk).aggregate(Sum('player1_score')).get('player1_score__sum') or 0
        s2 = rounds.filter(player2_id=player.pk).aggregate(Sum('player2_score')).get('player2_score__sum') or 0
        player.score = s1 + s2
        player.save()

def create_rounds(bracket_id, nuber_of_rounds):
    bracket = get_object_or_404(Bracket, pk=bracket_id)
    for i in range(1, nuber_of_rounds + 1):
        if Rounds.objects.filter(bracket=bracket, round=i).exists() == False:
            round = Rounds.objects.create(bracket=bracket, round=i, isFinished=False)
            round.save()

def add_players_to_round(bracket_id, round_id, player1_id, player2_id, player1_score=0, player2_score=0):
    round_obj = get_object_or_404(Rounds, pk=round_id)
    if round_obj.player1_id is None:
        round_obj.player1_id = player1_id
        round_obj.player1_score = player1_score
    if round_obj.player1_id is None:
        round_obj.player2_id = player2_id
        round_obj.player2_score = player2_score
    round_obj.save()

def create_round_and_add_players(bracket_id, round_number, player1_id, player2_id, player1_score=0, player2_score=0):
    bracket = get_object_or_404(Bracket, pk=bracket_id)
    round_obj, created  = Rounds.objects.get_or_create(bracket=bracket, round=round_number, isFinished=False, player1_id=player1_id, player2_id=player2_id)

    round_obj.save()


def sort_players(bracket_id, round):
    players = Player.objects.filter(bracket=bracket_id).all()

    # if round in rounds table get score from rounds table for each half of players and sort them by rating if round is 0 or score if round is > 0
    if round > 1:
        players = players.order_by("-score")
    else:
        players = players.order_by("-rating")

    # split players into two halves for each round
    first_half = players[:len(players)//2]
    second_half = players[len(players)//2:]
    return first_half, second_half
