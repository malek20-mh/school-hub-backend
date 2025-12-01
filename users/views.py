from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # تحقق من الرمز
            code = form.cleaned_data.get("code")
            if code != "123456":
                user.delete()
                messages.error(request, "❌ الرمز غير صحيح")
                return redirect("signup")

            login(request, user)
            messages.success(request, "تم إنشاء الحساب وتسجيل الدخول ✅")
            return redirect("stadium_list")  # 👈 هنا حلينا مشكلة NoReverseMatch
    else:
        form = CustomUserCreationForm()

    return render(request, "users/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول ✅")
            return redirect("stadium_list")  # 👈 هنا أيضًا
        else:
            messages.error(request, "❌ اسم المستخدم أو كلمة المرور غير صحيحة")
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج 👋")
    return redirect("login")