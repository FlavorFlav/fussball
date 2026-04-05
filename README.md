# Fussball Tracker

Django-based foosball score tracker with QR code sign-up.

## Dev Container Setup

1. Open this folder in VS Code
2. **Ctrl+Shift+P** → "Dev Containers: Reopen in Container"
3. Once inside the container, run:

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for admin access
python manage.py runserver 0.0.0.0:8000
```

4. Open http://localhost:8000

## Pages

| URL | Description |
|-----|-------------|
| `/` | Dashboard (login required) — your stats & match history |
| `/enter-score/` | Record a match result |
| `/leaderboard/` | Public leaderboard |
| `/signup/` | Create a new account |
| `/signup/qr/` | Display QR code linking to sign-up page |
| `/login/` | Login |
| `/admin/` | Django admin |
