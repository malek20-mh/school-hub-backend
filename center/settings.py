import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url  # <-- مكتبة ضرورية للربط مع Neon/Render

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# التعامل مع المفتاح السري ومتغير التصحيح بشكل آمن
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

# تحويل النص إلى بوليان لأن متغيرات البيئة تكون نصوص دائماً
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# السماح لجميع النطاقات مؤقتاً أو تحديد نطاق ريندر
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# مهم جداً عند الرفع على Render (HTTPS)
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "channels",
    # تطبيقاتك
    "apps.core",
    "stadiums",
    "users",
    "leagues",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <-- يجب أن يكون هنا مباشرة بعد Security
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "center.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "center.wsgi.application"
ASGI_APPLICATION = "center.asgi.application"

# --- إعدادات قاعدة البيانات ---
# محلياً: يستخدم القيم الافتراضية المكتوبة
# في السيرفر: يستخدم رابط DATABASE_URL الذي سنضيفه في Render
DATABASES = {
    "default": dj_database_url.config(
        default=f"postgres://{os.getenv('DB_USER', 'center_user')}:{os.getenv('DB_PASSWORD', '775165375')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'center')}",
        conn_max_age=600
    )
}

# --- إعدادات الملفات الثابتة (CSS/JS) ---
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# تفعيل ضغط الملفات وتسريعها باستخدام WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGOUT_REDIRECT_URL = "stadium_list"

# --- إعدادات Redis / Channels ---
# ملاحظة: ريندر المجاني لا يوفر Redis
# إذا لم تضع رابط Redis خارجي، هذه الميزات لن تعمل في العرض المجاني
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    }
}

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Aden"

# DRF
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "IBB Football Booking API",
    "VERSION": "0.1.0",
}

CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "0") == "1"

# Internationalization
LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Aden"
USE_I18N = True
USE_TZ = True