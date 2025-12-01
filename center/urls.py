from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("stadiums.urls")),  # فيه اسم 'stadium_list'
    path("", include("users.urls")),     # /signup /login /logout
      path("", include("leagues.urls")),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)