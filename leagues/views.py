from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import League, Match, GoalScorer, Team, Group, KnockoutMatch
from .forms import LeagueForm, MatchForm, TeamFormSet, GoalScorerFormSet,  GroupForm, TeamForm, KnockoutMatchForm
from django.forms import inlineformset_factory, modelformset_factory
from django.db.models import Sum , Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import math
from django.utils import timezone
# ---------------------------
# قائمة الدوريات
# ---------------------------
def league_list(request):
    leagues = League.objects.all().order_by("-created_at")
    return render(request, "leagues/league_list.html", {"leagues": leagues})

# ---------------------------
# حساب نقاط المواجهات المباشرة بين فريقين داخل دوري
# ---------------------------
def _h2h_points(team1, team2, league):
    """نقاط team1 أمام team2 داخل نفس الدوري (3 فوز / 1 تعادل / 0 خسارة)."""
    matches = Match.objects.filter(league=league).filter(
        models.Q(team_a=team1, team_b=team2) | models.Q(team_a=team2, team_b=team1)
    )
    pts = 0
    for m in matches:
        if m.goals_team_a is None or m.goals_team_b is None:
            continue
        if m.team_a == team1:
            if m.goals_team_a > m.goals_team_b:
                pts += 3
            elif m.goals_team_a == m.goals_team_b:
                pts += 1
        else:  # team1 كان B
            if m.goals_team_b > m.goals_team_a:
                pts += 3
            elif m.goals_team_b == m.goals_team_a:
                pts += 1
    return pts

# ---------------------------
# تفاصيل الدوري + جدول الترتيب
# ---------------------------
def league_detail(request, pk):
    league = get_object_or_404(League, pk=pk)
    groups = league.groups.all()

    league_standings = []
    for group in groups:
        teams = list(group.teams.all())
        standings = []
        for team in teams:
            matches_a = Match.objects.filter(team_a=team, league=league)
            matches_b = Match.objects.filter(team_b=team, league=league)

            played = wins = draws = losses = 0
            goals_for = goals_against = 0

            for m in matches_a:
                if m.goals_team_a is not None and m.goals_team_b is not None:
                    played += 1
                    goals_for += m.goals_team_a
                    goals_against += m.goals_team_b
                    if m.goals_team_a > m.goals_team_b:
                        wins += 1
                    elif m.goals_team_a == m.goals_team_b:
                        draws += 1
                    else:
                        losses += 1

            for m in matches_b:
                if m.goals_team_a is not None and m.goals_team_b is not None:
                    played += 1
                    goals_for += m.goals_team_b
                    goals_against += m.goals_team_a
                    if m.goals_team_b > m.goals_team_a:
                        wins += 1
                    elif m.goals_team_b == m.goals_team_a:
                        draws += 1
                    else:
                        losses += 1

            points = wins * 3 + draws
            standings.append({
                "team": team,
                "played": played,
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "points": points,
                "goals_for": goals_for,
                "goals_against": goals_against,
                "goal_diff": goals_for - goals_against,
            })

        standings.sort(key=lambda x: (-x["points"], -x["goal_diff"], -x["goals_for"], x["team"].name.lower()))
        league_standings.append((group.name, standings))

    return render(request, "leagues/league_detail.html", {
        "league": league,
        "league_standings": league_standings,
    })
    # ---------------------------
# جدول المباريات
# ---------------------------
def league_matches(request, pk):
    league = get_object_or_404(League, pk=pk)
    matches = league.matches.all().order_by("date")
    return render(request, "leagues/league_matches.html", {"league": league, "matches": matches})

# ---------------------------
# قائمة الهدافين
# ---------------------------
def league_scorers(request, pk):
    league = get_object_or_404(League, pk=pk)
    
    # نقوم بتجميع الأهداف حسب اسم اللاعب والفريق
    scorers = GoalScorer.objects.filter(match__league=league) \
        .values('player_name', 'team__name', 'team__logo') \
        .annotate(total_goals=Sum('goals')) \
        .order_by('-total_goals')

    return render(request, "leagues/league_scorers.html", {"league": league, "scorers": scorers})
# ---------------------------
# إنشاء دوري
# ---------------------------
@login_required
def league_create(request):
    if request.method == "POST":
        form = LeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.owner = request.user   # ⬅️ لازم نعين المستخدم الحالي كـ owner
            league.save()

            formset = GroupFormSet(request.POST, instance=league)
            if formset.is_valid():
                formset.save()

            return redirect("team_add", league_id=league.pk)
    else:
        form = LeagueForm()
        formset = GroupFormSet()

    return render(request, "leagues/league_create.html", {
        "form": form,
        "formset": formset,
    })
GroupFormSet = inlineformset_factory(
    League, Group, form=GroupForm, extra=1, can_delete=True
)

TeamFormSet = inlineformset_factory(
    League, Team, form=TeamForm, extra=1, can_delete=True
)
# ---------------------------
# تعديل دوري
# ---------------------------


GroupFormSet = inlineformset_factory(
    League, Group, form=GroupForm, extra=1, can_delete=True
)

TeamFormSet = inlineformset_factory(
    League, Team, form=TeamForm, extra=1, can_delete=True
)

@login_required
def league_update(request, pk):
    league = get_object_or_404(League, pk=pk)

    if request.method == "POST":
        form = LeagueForm(request.POST, instance=league)
        group_formset = GroupFormSet(request.POST, instance=league)
        if form.is_valid() and group_formset.is_valid():
            form.save()
            group_formset.save()
            return redirect("league_detail", pk=league.pk)
    else:
        form = LeagueForm(instance=league)
        group_formset = GroupFormSet(instance=league)
    return render(
        request,
        "leagues/league_update.html",
        {
            "form": form,
            "group_formset": group_formset,
            "league": league,
        },
    )
# ---------------------------
# حذف دوري
# ---------------------------
def league_delete(request, pk):
    league = get_object_or_404(League, pk=pk)
    if request.user != league.owner:
        return HttpResponseForbidden("🚫 لا تملك صلاحية حذف هذا الدوري")

    if request.method == "POST":
        league.delete()
        return redirect("league_list")
    return render(request, "leagues/league_delete_confirm.html", {"league": league})

@login_required
def match_create(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    if request.user != league.owner:
        return HttpResponseForbidden("🚫 لا تملك صلاحية إضافة مباراة في هذا الدوري")

    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.league = league
            match.save()
            return redirect("league_matches", pk=league.id)
    else:
        form = MatchForm()
    return render(request, "leagues/match_form.html", {"form": form, "league": league})


@login_required
def match_update(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.user != match.league.owner:
        return HttpResponseForbidden("🚫 لا تملك صلاحية تعديل هذه المباراة")

    if request.method == "POST":
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect("league_matches", pk=match.league.id)
    else:
        form = MatchForm(instance=match)
    return render(request, "leagues/match_form.html", {"form": form, "league": match.league})


@login_required
def match_delete(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.user != match.league.owner:
        return HttpResponseForbidden("🚫 لا تملك صلاحية حذف هذه المباراة")

    if request.method == "POST":
        league_id = match.league.id
        match.delete()
        return redirect("league_matches", pk=league_id)
    return render(request, "leagues/match_delete.html", {"match": match})

from django.core.paginator import Paginator # <-- لا تنسَ هذا الاستيراد في أعلى الملف

@login_required
def league_scorers_update(request, pk):
    league = get_object_or_404(League, pk=pk)
    if request.user != league.owner:
        return HttpResponseForbidden("🚫 لا تملك صلاحية تعديل هدافي هذا الدوري")

    # 1. جلب المباريات (الأحدث أولاً)
    all_matches = league.matches.all().order_by('-date')

    # 2. تقسيم الصفحات (جربنا 5، ويمكنك زيادتها الآن لأن القوائم أصبحت خفيفة)
    paginator = Paginator(all_matches, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    formsets = []

    if request.method == "POST":
        all_valid = True
        for match in page_obj:
            formset = GoalScorerFormSet(
                request.POST, request.FILES,
                instance=match,
                prefix=str(match.id)
            )
            
            # 🔥 السطر السحري: تحديد الفريقين فقط في القائمة (للفحص)
            match_teams = Team.objects.filter(id__in=[match.team_a.id, match.team_b.id])
            for form in formset:
                form.fields['team'].queryset = match_teams
            
            formsets.append((match, formset))
            if not formset.is_valid():
                all_valid = False

        if all_valid:
            for match, formset in formsets:
                formset.save()
            
            # العودة لنفس الصفحة
            current_page = request.GET.get('page', 1)
            return redirect(f"{reverse('league_scorers_update', args=[league.pk])}?page={current_page}")

    else:
        for match in page_obj:
            formset = GoalScorerFormSet(
                instance=match,
                prefix=str(match.id)
            )
            
            # 🔥 السطر السحري: تحديد الفريقين فقط في القائمة (للعرض)
            # 1. نحدد الفريقين الخاصين بهذه المباراة فقط
            match_teams = Team.objects.filter(id__in=[match.team_a.id, match.team_b.id])
            
            # 2. نطبق هذا التحديد على جميع الخانات الموجودة (للأهداف المسجلة سابقاً)
            for form in formset.forms:
                form.fields['team'].queryset = match_teams
            
            # 3. نطبق هذا التحديد على "الخانات الفارغة" (زر إضافة جديد)
            formset.empty_form.fields['team'].queryset = match_teams

            formsets.append((match, formset))

    return render(request, "leagues/league_scorers_update.html", {
        "league": league,
        "formsets": formsets,
        "page_obj": page_obj,
    })

@login_required
def team_add(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    TeamFormSet = modelformset_factory(Team, form=TeamForm, extra=3, can_delete=True)

    if request.method == "POST":
        formset = TeamFormSet(request.POST, request.FILES, queryset=Team.objects.filter(group__league=league))
        if formset.is_valid():
            teams = formset.save(commit=False)
            for team in teams:
                # إذا الدوري فيه مجموعة واحدة فقط وما اختار المستخدم
                if league.groups.count() == 1 and not team.group:
                    team.group = league.groups.first()
                team.save()

            # حذف الفرق اللي تم تحديدها للحذف
            for obj in formset.deleted_objects:
                obj.delete()

            return redirect("league_detail", pk=league.pk)
    else:
        formset = TeamFormSet(queryset=Team.objects.filter(group__league=league))

    return render(request, "leagues/team_add.html", {
        "league": league,
        "formset": formset,
    })

# leagues/views.py


# ... باقي دوال العرض الخاصة بك ...

def match_detail(request, match_id):
    # جلب المباراة المحددة أو إظهار خطأ 404 إذا لم توجد
    match = get_object_or_404(Match, id=match_id)
    
    # إرسال كائن "match" إلى القالب
    context = {
        'match': match
    }
    return render(request, 'leagues/match_detail.html', context) # تأكد من أن المسار صحيح

def generate_matches_card(request):
    """
    تستقبل قائمة معرّفات المباريات (IDs) من نموذج POST
    وتعرضها في قائمة مرتبة قابلة للتصوير كجدول.
    """
    if request.method == 'POST':
        # الحصول على قائمة IDs للمباريات التي تم تحديدها
        selected_ids = request.POST.getlist('selected_matches')
        
        # التأكد من وجود معرفات تم إرسالها
        if not selected_ids:
            # يمكن توجيه المستخدم لصفحة خطأ أو رسالة تنبيه
            # هنا سنقوم بتوجيهه إلى صفحة الدوريات
            return redirect('league_list') 

        # جلب المباريات المختارة فقط وترتيبها حسب التاريخ
        matches = Match.objects.filter(id__in=selected_ids).order_by('date')
        
        # التأكد من وجود مباريات بعد التصفية
        if not matches:
             return redirect('league_list') 
        
        # بما أن القالب يحتاج معلومات الدوري (للعنوان)
        # نأخذ معلومات الدوري من أول مباراة في القائمة
        league = matches.first().league
        
        context = {
            'matches': matches,
            'league': league,
        }
        
        # عرض القالب الجديد الذي سنقوم بإنشائه في الخطوة القادمة
        return render(request, 'leagues/matches_export_card.html', context)
        
    # إذا لم يكن الطلب POST (مثل الوصول المباشر للرابط)، نوجه المستخدم
    return redirect('league_list')


def knockout_setup(request, league_id):
    league = get_object_or_404(League, id=league_id)
    
    if request.method == 'POST':
        selected_team_ids = request.POST.getlist('selected_teams')
        count = len(selected_team_ids)
        
        if count not in [4, 8, 16, 32]:
            messages.error(request, f"العدد ({count}) غير مدعوم حالياً. اختر 4، 8، 16، أو 32.")
            return redirect('knockout_setup', league_id=league.id)

        # 1. تنظيف الشجرة القديمة
        KnockoutMatch.objects.filter(league=league).delete()

        # 2. جلب الفرق المختارة
        teams = Team.objects.filter(id__in=selected_team_ids)
        
        # 3. تجميع الفرق حسب المجموعات وترتيبهم داخل المجموعة
        # سنفترض أن المجموعات لها أسماء أو معرفات. سنرتب حسب النقاط.
        teams_by_group = {}
        for team in teams:
            g_id = team.group.id if team.group else 0
            if g_id not in teams_by_group:
                teams_by_group[g_id] = []
            teams_by_group[g_id].append(team)

        # ترتيب الفرق داخل كل مجموعة (الأول، الثاني...)
        for g_id in teams_by_group:
            # ترتيب حسب النقاط تنازلياً (يمكنك إضافة فارق الأهداف هنا)
            teams_by_group[g_id].sort(key=lambda x: getattr(x, 'points', 0), reverse=True)

        # 4. خوارزمية التزويج (Pairing Algorithm)
        matchups = []
        groups_ids = list(teams_by_group.keys())
        
        # سيناريو 4 فرق (نصف نهائي مباشرة)
        if count == 4 and len(groups_ids) >= 2:
            # الأول من A ضد الثاني من B
            g1 = teams_by_group[groups_ids[0]]
            g2 = teams_by_group[groups_ids[1]]
            # التأكد من وجود فريقين في كل مجموعة
            if len(g1) >= 2 and len(g2) >= 2:
                matchups.append((g1[0], g2[1])) # 1st A vs 2nd B
                matchups.append((g2[0], g1[1])) # 1st B vs 2nd A
            else:
                # توزيع عشوائي إذا لم تكتمل الشروط
                matchups.append((g1[0], g2[0]))
                matchups.append((g1[1] if len(g1)>1 else g2[1], g2[1] if len(g2)>1 else g1[1]))

        # سيناريو 8 فرق أو أكثر (نظام المقص: الأول ضد الأخير)
        else:
            # دمج القوائم بطريقة تسمح بالمواجهة العكسية
            # سنقوم بجمع كل "الأوائل" وكل "الثواني" ...
            # الطريقة الأبسط والأشهر: دمج المجموعات المتقابلة (A مع B)
            
            processed_groups = []
            for i in range(0, len(groups_ids), 2):
                if i+1 < len(groups_ids):
                    gA = teams_by_group[groups_ids[i]]
                    gB = teams_by_group[groups_ids[i+1]]
                    
                    # عدد المتأهلين من كل مجموعة
                    n = len(gA) 
                    for j in range(n):
                        # الأول (index 0) يواجه الأخير (index n-1-j)
                        # مثال: 4 فرق. 0 vs 3, 1 vs 2
                        if j < len(gB):
                            t1 = gA[j]
                            t2 = gB[len(gB)-1-j] # عكسي من المجموعة الأخرى
                            matchups.append((t1, t2))
                else:
                    # مجموعة فردية بقيت (نادرة)، نزاوجها داخلياً
                    g = teams_by_group[groups_ids[i]]
                    for j in range(len(g)//2):
                        matchups.append((g[j], g[len(g)-1-j]))

        # 5. إنشاء المباريات في قاعدة البيانات
        round_name = count
        current_matches_objs = []
        
        for i, (t1, t2) in enumerate(matchups):
            m = KnockoutMatch.objects.create(
                league=league,
                round_number=round_name,
                match_order=i+1,
                team1=t1,
                team2=t2
            )
            current_matches_objs.append(m)

        # 6. إنشاء الأدوار التالية فارغة (الهيكل العظمي للشجرة)
        previous_round_matches = current_matches_objs
        next_round = count // 2
        
        while next_round >= 2: # 2 يعني النهائي
            new_round_matches = []
            for i in range(0, len(previous_round_matches), 2):
                next_match = KnockoutMatch.objects.create(
                    league=league,
                    round_number=next_round,
                    match_order=(i // 2) + 1
                )
                
                # ربط الفائزين
                if i < len(previous_round_matches):
                    previous_round_matches[i].next_match = next_match
                    previous_round_matches[i].save()
                
                if i+1 < len(previous_round_matches):
                    previous_round_matches[i+1].next_match = next_match
                    previous_round_matches[i+1].save()
                
                new_round_matches.append(next_match)
            
            previous_round_matches = new_round_matches
            next_round //= 2

        messages.success(request, "تم إنشاء الشجرة بنظام المواجهات العكسية (المقص) ✂️")
        return redirect('league_knockout', league_id=league.id)

    # GET Request
    all_teams = list(Team.objects.filter(league=league))
    # ترتيب للعرض فقط
    try:
        all_teams.sort(key=lambda t: (t.group.name if t.group else '', -getattr(t, 'points', 0)))
    except:
        all_teams.sort(key=lambda t: (t.group.name if t.group else '', t.name))
        
    return render(request, 'leagues/knockout_setup.html', {'league': league, 'teams': all_teams})
# فيو لعرض الشجرة
def publish_knockout(request, league_id):
    league = get_object_or_404(League, id=league_id)
    if request.user != league.owner:
        return redirect('league_knockout', league_id=league.id)
    
    if request.method == 'POST':
        # جلب مباريات الشجرة التي لها أطراف (ليست فارغة)
        ko_matches = KnockoutMatch.objects.filter(league=league).exclude(team1=None).exclude(team2=None)
        
        count = 0
        for ko in ko_matches:
            # التحقق مما إذا كانت موجودة مسبقاً في الجدول الرئيسي لتجنب التكرار
            # يمكنك استخدام منطق للتحقق، هنا سنضيفها ببساطة
            
            Match.objects.create(
                league=league,
                home_team=ko.team1,
                away_team=ko.team2,
                date=timezone.now(), # تاريخ افتراضي، يجب تعديله لاحقاً
                round_name=ko.get_round_number_display(),
                is_finished=False
            )
            count += 1
            
        messages.success(request, f"تم نشر {count} مباراة إلى جدول المباريات الرئيسي بنجاح! ✅")
        return redirect('league_matches', league_id=league.id)


def publish_knockout_to_main(request, league_id):
    league = get_object_or_404(League, id=league_id)
    if request.user != league.owner:
        return redirect('league_knockout', league_id=league.id)

    if request.method == 'POST':
        ko_matches = KnockoutMatch.objects.filter(league=league).exclude(team1=None).exclude(team2=None)
        count = 0
        
        for ko in ko_matches:
            # دمج التاريخ والوقت ليناسب حقل date في Match (إذا كان DateTimeField)
            # أو تركهما منفصلين حسب تصميم موديل Match لديك
            # سنفترض هنا أن Match.date هو DateTimeField
            
            match_datetime = timezone.now() # افتراضي
            if ko.date:
                t = ko.time if ko.time else time(0,0) # وقت افتراضي منتصف الليل
                match_datetime = datetime.combine(ko.date, t)
                # جعل التوقيت واعي (Aware) للمنطقة الزمنية
                match_datetime = timezone.make_aware(match_datetime)

            # التحقق من التكرار
            exists = Match.objects.filter(
                league=league,
                home_team=ko.team1,
                away_team=ko.team2,
                round_name=ko.get_round_number_display()
            ).exists()

            if not exists:
                Match.objects.create(
                    league=league,
                    home_team=ko.team1,
                    away_team=ko.team2,
                    date=match_datetime, # ✅ التاريخ من الشجرة
                    stadium=ko.location, # ✅ المكان من الشجرة (تأكد أن موديل Match فيه حقل stadium أو location)
                    round_name=ko.get_round_number_display(),
                    is_finished=False
                )
                count += 1
        
        messages.success(request, f"تم اعتماد {count} مباراة في الجدول الرسمي!")
        return redirect('league_matches', league_id=league.id)
        
    return redirect('league_knockout', league_id=league.id)

def edit_knockout_match(request, match_id):
    match = get_object_or_404(KnockoutMatch, id=match_id)
    
    # حماية: المالك فقط
    if request.user != match.league.owner:
        return redirect('league_knockout', league_id=match.league.id)

    if request.method == 'POST':
        form = KnockoutMatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث بيانات المباراة بنجاح ✅")
            return redirect('league_knockout', league_id=match.league.id)
    else:
        form = KnockoutMatchForm(instance=match)

    return render(request, 'leagues/knockout_edit.html', {'form': form, 'match': match})

# أضف هذا في نهاية ملف leagues/views.py

def league_knockout(request, league_id):
    league = get_object_or_404(League, id=league_id)
    matches = KnockoutMatch.objects.filter(league=league).order_by('-round_number', 'match_order')
    
    # تجميع المباريات حسب رقم الدور (16, 8, 4, 2) لسهولة العرض في القالب
    rounds = {}
    for match in matches:
        r_num = match.round_number
        if r_num not in rounds:
            rounds[r_num] = []
        rounds[r_num].append(match)
        
    return render(request, 'leagues/knockout_view.html', {'league': league, 'rounds': rounds})