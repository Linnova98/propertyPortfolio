from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('api/property/', include('property.urls')),
    path('api/portfolio/', include('portfolio.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
