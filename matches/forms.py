from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player, Match


class SignupForm(UserCreationForm):
    display_name = forms.CharField(max_length=100, help_text="Your display name for the leaderboard")

    class Meta:
        model = User
        fields = ("username", "display_name", "password1", "password2")


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ("player_away", "score_home", "score_away")
        labels = {
            "player_away": "Opponent",
            "score_home": "Your score",
            "score_away": "Opponent's score",
        }

    def __init__(self, *args, current_player=None, **kwargs):
        super().__init__(*args, **kwargs)
        if current_player:
            self.fields["player_away"].queryset = Player.objects.exclude(pk=current_player.pk)
