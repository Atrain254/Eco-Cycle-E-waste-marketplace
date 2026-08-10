from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings             # <-- Ensure this is imported
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('marketplace/', include('marketplace.urls')),
    path('', RedirectView.as_view(url='/marketplace/', permanent=True)), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)