from django import forms
from django.forms import inlineformset_factory
from .models import League, Team, Match, GoalScorer, Group  

# ---------------------------
# League Form
# ---------------------------
class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ["name", "location","logo"]


# ---------------------------
# Team Form
# ---------------------------
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "logo", "group"]

    def __init__(self, *args, **kwargs):
        league = kwargs.pop("league", None)
        super().__init__(*args, **kwargs)
        if league:
            self.fields["group"].queryset = Group.objects.filter(league=league)
        else:
            self.fields["group"].queryset = Group.objects.none()
# ---------------------------
# Match Form
# ---------------------------
class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            "team_a", "team_b", "date", "stadium",
            "goals_team_a", "goals_team_b",
            "yellow_cards_team_a", "yellow_cards_team_b",
            "red_cards_team_a", "red_cards_team_b"
        ]


# ---------------------------
# Inline Formset for Teams
# ---------------------------
TeamFormSet = inlineformset_factory(
    League, Team,
    form=TeamForm,
    fields=["name", "logo", "group"],
    extra=1,        # عدد الصفوف الفارغة لإضافة فرق جديدة
    can_delete=True # يتيح حذف الفرق
)
GoalScorerFormSet = inlineformset_factory(
    Match, GoalScorer,
    fields=["player_name", "team", "goals"],
    extra=1,
    can_delete=True
)
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]  # إذا عندك حقول إضافية ضيفها

