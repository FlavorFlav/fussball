from datetime import date

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
        fields = ("player_away", "score_home", "score_away", "played_at")
        labels = {
            "player_away": "Opponent",
            "score_home": "Your score",
            "score_away": "Opponent's score",
            "played_at": "Date",
        }
        widgets = {
            "played_at": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def __init__(self, *args, current_player=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["played_at"].widget.attrs["max"] = date.today().isoformat()
        self.fields["played_at"].initial = date.today()
        self.fields["player_away"].empty_label = "Select opponent"
        if current_player:
            self.fields["player_away"].queryset = Player.objects.exclude(pk=current_player.pk)

    def clean(self):
        cleaned = super().clean()
        home = cleaned.get("score_home")
        away = cleaned.get("score_away")
        if home is not None and away is not None:
            high = max(home, away)
            low = min(home, away)
            if home == away:
                raise forms.ValidationError("Ties are not allowed.")
            if high < 10:
                raise forms.ValidationError("The winning score must be at least 10.")
            if low <= 8 and high != 10:
                raise forms.ValidationError("When the losing score is 8 or less, the winning score must be exactly 10.")
            if low >= 9 and high != low + 2:
                raise forms.ValidationError("At deuce (9+), the winner must lead by exactly 2.")
        return cleaned
