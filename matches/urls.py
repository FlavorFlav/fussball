from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("signup/qr/", views.signup_qr, name="signup_qr"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("enter-score/", views.enter_score, name="enter_score"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
