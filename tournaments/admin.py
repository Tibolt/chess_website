from django.contrib import admin
from .models import Player, Bracket, Rounds

# Register your models here.


class PlayerInLine(admin.TabularInline):
    model = Player


class BracketAdmin(admin.ModelAdmin):
    inlines = [PlayerInLine]  # allows to add players in bracket table

    class Meta:
        model = Bracket


admin.site.register(Bracket, BracketAdmin)
admin.site.register(Player)
admin.site.register(Rounds)
