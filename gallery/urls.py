from django.urls import path
from .views import gallery, gallery_page

urlpatterns = [
    path('', gallery, name='gallery'),
    path('<slug:gallery_url>/', gallery_page, name='gallery_page')
]
