from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from app.views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),

    path('matriculas/', include('matriculas.urls')),
    path('materiais/', include('materiais.urls')),
]

if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
