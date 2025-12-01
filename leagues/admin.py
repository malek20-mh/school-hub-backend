from django.contrib import admin
from .models import League, Group, Team, Match, GoalScorer


# ---------------------------
# Inline لإدارة المجموعات والفرق من داخل الدوري
# ---------------------------
class GroupInline(admin.TabularInline):
    model = Group
    extra = 1


class TeamInline(admin.TabularInline):
    model = Team
    extra = 1


# ---------------------------
# League
# ---------------------------
@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "created_at")
    search_fields = ("name", "owner__username")
    inlines = [GroupInline, TeamInline]


# ---------------------------
# Group
# ---------------------------
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "league")
    search_fields = ("name", "league__name")


# ---------------------------
# Team
# ---------------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "league", "group")
    search_fields = ("name", "league__name")


# ---------------------------
# Match
# ---------------------------
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "league", "team_a", "team_b", "date", "stadium",
        "goals_team_a", "goals_team_b",
        "yellow_cards_team_a", "yellow_cards_team_b",
        "red_cards_team_a", "red_cards_team_b"
    )
    list_filter = ("league", "date")


# ---------------------------
# GoalScorer
# ---------------------------
@admin.register(GoalScorer)
class GoalScorerAdmin(admin.ModelAdmin):
    list_display = ("player_name", "team", "goals", "match")
    search_fields = ("player_name", "team__name")