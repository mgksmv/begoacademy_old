from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home, contacts
from seminars.views import past_seminars, seminar_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('seminars/', include('seminars.urls')),
    path('past-seminars/', include('seminars.past_urls')),
    path('individual/', include('individual.urls')),
    path('lectors/', include('lectors.urls')),
    path('gallery/', include('gallery.urls')),
    path('contacts/', contacts, name='contacts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'config.views.error_404'
