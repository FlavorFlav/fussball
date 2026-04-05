from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("qr/", views.enter_score_qr, name="qr"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("enter-score/", views.enter_score, name="enter_score"),
    path("edit-match/<int:match_id>/", views.edit_match, name="edit_match"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
