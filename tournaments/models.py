from django.db import models
# Create your models here.


class Bracket(models.Model):
    size = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=200)
    date = models.DateTimeField(
        'tournament date',
        null=True,
        blank=True
    )
    numberOfRounds = models.PositiveIntegerField(default=1)

    def __str__(self):
        date = str(self.date) if self.date else ""
        return str(self.name) + " " + date


class Player(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    score = models.FloatField(
        default=0,
        null=True,
    )
    score_round = models.FloatField(
        default=0,
        null=True,
    )
    bracket = models.ForeignKey(
        Bracket,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )  # many to one relation

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Rounds(models.Model):
    round = models.PositiveIntegerField(default=1)
    player1_id = models.PositiveIntegerField(null=True, blank=True)
    player2_id = models.PositiveIntegerField(null=True, blank=True)
    player1_score = models.FloatField(null=True, default=0)
    player2_score = models.FloatField(null=True, default=0)
    bracket = models.ForeignKey(
        Bracket,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    isFinished = models.BooleanField(default=False)

    def __str__(self):
        player1_name = Player.objects.get(pk=self.player1_id).name if self.player1_id else ""
        player2_name = Player.objects.get(pk=self.player2_id).name if self.player2_id else ""

        return f"{self.bracket.name} {self.round} | {player1_name} vs {player2_name}"
