from django.db import models
from django.contrib.auth.models import User

class League(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leagues")
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.URLField(max_length=500, null=True, blank=True, verbose_name="رابط شعار الدوري")
    def __str__(self):
        return self.name

class Group(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.league.name}"

class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="teams", null=True, blank=True)
    name = models.CharField(max_length=200)
    logo = models.URLField(max_length=500, blank=True, null=True, verbose_name="رابط شعار الفريق")

    def __str__(self):
        return f"{self.name} ({self.league.name})"


class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="matches")
    team_a = models.ForeignKey(Team, related_name="team_a_matches", on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name="team_b_matches", on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True, default=None)
    stadium = models.CharField(max_length=100)

    # اختيارية لعدم لعب المباراة بعد
    goals_team_a = models.IntegerField(null=True, blank=True, default=None)
    goals_team_b = models.IntegerField(null=True, blank=True, default=None)
    yellow_cards_team_a = models.IntegerField(null=True, blank=True, default=None)
    yellow_cards_team_b = models.IntegerField(null=True, blank=True, default=None)
    red_cards_team_a = models.IntegerField(null=True, blank=True, default=None)
    red_cards_team_b = models.IntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.team_a} vs {self.team_b} ({self.league})"


class GoalScorer(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="goals")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="scorers")
    player_name = models.CharField(max_length=200)
    goals = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.player_name} - {self.goals} أهداف"