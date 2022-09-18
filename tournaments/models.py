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


class Player(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    score = models.PositiveIntegerField(
        default=0,
        null=True,
    )
    bracket = models.ForeignKey(
        Bracket,
        on_delete=models.CASCADE,
    )  # many to one relation

    def __str__(self):
        return str(self.name) + " " + str(self.last_name)
