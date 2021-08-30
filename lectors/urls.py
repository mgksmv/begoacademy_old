from django.urls import path
from .views import lectors, lector_page

urlpatterns = [
    path('', lectors, name='lectors'),
    path('<slug:lector_url>', lector_page, name='lector_page')
]
