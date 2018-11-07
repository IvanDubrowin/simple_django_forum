from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from main_app.admin import admin_site
from forum import settings


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include(('main_app.urls', 'main'), namespace='main')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
