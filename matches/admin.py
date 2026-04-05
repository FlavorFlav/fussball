from django.contrib import admin
from .models import Player, Match


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "created_at")
    readonly_fields = ("signup_token",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("player_home", "score_home", "score_away", "player_away", "played_at")
    list_filter = ("played_at",)
