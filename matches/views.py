import base64
from io import BytesIO

import qrcode
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import F, Sum, Count, Q, Case, When, IntegerField
from django.shortcuts import redirect, render

from .forms import MatchForm, SignupForm
from .models import Match, Player


def signup_qr(request):
    """Display a QR code that links to the signup page."""
    signup_url = "http://192.168.1.9:8000/signup/"
    img = qrcode.make(signup_url, box_size=8, border=2)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()
    return render(request, "matches/signup_qr.html", {"qr_b64": qr_b64, "signup_url": signup_url})


def signup(request):
    """Register a new player account."""
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Player.objects.create(user=user, display_name=form.cleaned_data["display_name"])
            login(request, user)
            messages.success(request, "Welcome! You're signed up.")
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "matches/signup.html", {"form": form})


@login_required
def dashboard(request):
    """Show the logged-in player's stats and match history."""
    player = request.user.player
    matches = Match.objects.filter(Q(player_home=player) | Q(player_away=player))[:20]
    return render(request, "matches/dashboard.html", {
        "player": player,
        "matches": matches,
    })


@login_required
def enter_score(request):
    """Let a player record a match result."""
    player = request.user.player
    if request.method == "POST":
        form = MatchForm(request.POST, current_player=player)
        if form.is_valid():
            match = form.save(commit=False)
            match.player_home = player
            match.save()
            messages.success(request, "Match recorded!")
            return redirect("dashboard")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = MatchForm(current_player=player)
    return render(request, "matches/enter_score.html", {"form": form})


def leaderboard(request):
    """Public leaderboard ranked by wins."""
    players = Player.objects.annotate(
        total_wins=Count(
            Case(
                When(home_matches__score_home__gt=F("home_matches__score_away"), then=1),
                output_field=IntegerField(),
            )
        ) + Count(
            Case(
                When(away_matches__score_away__gt=F("away_matches__score_home"), then=1),
                output_field=IntegerField(),
            )
        ),
        total_matches=Count("home_matches", distinct=True) + Count("away_matches", distinct=True),
    ).order_by("-total_wins")
    return render(request, "matches/leaderboard.html", {"players": players})


class CustomLoginView(LoginView):
    template_name = "matches/login.html"


class CustomLogoutView(LogoutView):
    next_page = "/"
