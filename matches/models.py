import uuid
from django.conf import settings
from django.db import models


class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="player")
    display_name = models.CharField(max_length=100)
    signup_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name

    @property
    def wins(self):
        return self.home_matches.filter(score_home__gt=models.F("score_away")).count() + \
               self.away_matches.filter(score_away__gt=models.F("score_home")).count()

    @property
    def losses(self):
        return self.home_matches.filter(score_home__lt=models.F("score_away")).count() + \
               self.away_matches.filter(score_away__lt=models.F("score_home")).count()

    @property
    def draws(self):
        return self.home_matches.filter(score_home=models.F("score_away")).count() + \
               self.away_matches.filter(score_away=models.F("score_home")).count()

    @property
    def total_matches(self):
        return self.home_matches.count() + self.away_matches.count()

    @property
    def goals_scored(self):
        home = self.home_matches.aggregate(total=models.Sum("score_home"))["total"] or 0
        away = self.away_matches.aggregate(total=models.Sum("score_away"))["total"] or 0
        return home + away

    @property
    def goals_conceded(self):
        home = self.home_matches.aggregate(total=models.Sum("score_away"))["total"] or 0
        away = self.away_matches.aggregate(total=models.Sum("score_home"))["total"] or 0
        return home + away


class Match(models.Model):
    player_home = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="home_matches")
    player_away = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="away_matches")
    score_home = models.PositiveIntegerField()
    score_away = models.PositiveIntegerField()
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-played_at"]
        verbose_name_plural = "matches"

    def __str__(self):
        return f"{self.player_home} {self.score_home} - {self.score_away} {self.player_away}"
