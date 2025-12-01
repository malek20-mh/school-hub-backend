from django.urls import path
from . import views

urlpatterns = [
    path("", views.league_list, name="league_list"),
    path("create/", views.league_create, name="league_create"),
    path("<int:pk>/", views.league_detail, name="league_detail"),
    path("<int:pk>/edit/", views.league_update, name="league_update"),
    path("<int:pk>/delete/", views.league_delete, name="league_delete"),
    path("<int:pk>/matches/", views.league_matches, name="league_matches"),
    path("<int:pk>/scorers/", views.league_scorers, name="league_scorers"),
    path("<int:league_id>/match/add/", views.match_create, name="match_create"),
    path("match/<int:pk>/edit/", views.match_update, name="match_update"),
    path("match/<int:pk>/delete/", views.match_delete, name="match_delete"),
    path("<int:pk>/scorers/edit/", views.league_scorers_update, name="league_scorers_update"),
    path("league/<int:league_id>/teams/add/", views.team_add, name="team_add"),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('matches/card/generate/', views.generate_matches_card, name='generate_matches_card'),
]