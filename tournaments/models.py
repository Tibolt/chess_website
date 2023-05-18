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
        return str(self.name) + " " + str(self.last_name)


class Rounds(models.Model):
    round = models.PositiveIntegerField()
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

