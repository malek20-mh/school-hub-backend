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

class KnockoutMatch(models.Model):
    ROUND_CHOICES = (
        (32, 'دور الـ 32'),
        (16, 'دور الـ 16'),
        (8, 'ربع النهائي'),
        (4, 'نصف النهائي'),
        (2, 'النهائي'),
        (1, 'البطل'), # اختياري
    )

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='knockout_matches')
    round_number = models.IntegerField(choices=ROUND_CHOICES) # مثال: 8 يعني ربع النهائي
    match_order = models.IntegerField() # ترتيب المباراة في الشجرة (1, 2, 3...)
    
    # الفرق (يمكن أن تكون فارغة في البداية حتى يتأهلوا)
    team1 = models.ForeignKey(Team, related_name='ko_home_matches', null=True, blank=True, on_delete=models.SET_NULL)
    team2 = models.ForeignKey(Team, related_name='ko_away_matches', null=True, blank=True, on_delete=models.SET_NULL)
    
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    winner = models.ForeignKey(Team, related_name='ko_wins', null=True, blank=True, on_delete=models.SET_NULL)
    
    # الرابط السحري للشجرة: الفائز في هذه المباراة يذهب إلى أي مباراة؟
    next_match = models.ForeignKey('self', null=True, blank=True, related_name='previous_matches', on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.league.name} - {self.get_round_number_display()} - Match {self.match_order}"