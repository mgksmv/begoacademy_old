from django.urls import path
from .views import for_dentists, for_tech, for_clinics, individual_page

urlpatterns = [
    path('for-dentists/', for_dentists, name='for_dentists'),
    path('for-tech/', for_tech, name='for_tech'),
    path('for-clinics/', for_clinics, name='for_clinics'),
    path('for-dentists/<slug:individual_url>/', individual_page, name='individual_page'),
    path('for-tech/<slug:individual_url>/', individual_page, name='individual_page'),
    path('for-clinics/<slug:individual_url>/', individual_page, name='individual_page'),
]
