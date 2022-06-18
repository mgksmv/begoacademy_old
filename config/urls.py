from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('seminars/', include('seminars.urls')),
    path('past-seminars/', include('seminars.past_urls')),
    path('individual/', include('individual.urls')),
    path('lectors/', include('lectors.urls')),
    path('gallery/', include('gallery.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

handler404 = 'main.views.error_404'
