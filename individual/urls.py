from django.urls import path
from .views import ForDentistsListView, ForTechListView, ForClinicsListView, individual_page

urlpatterns = [
    path('for-dentists/', ForDentistsListView.as_view(), name='for_dentists'),
    path('for-tech/', ForTechListView.as_view(), name='for_tech'),
    path('for-clinics/', ForClinicsListView.as_view(), name='for_clinics'),
    path('for-dentists/<slug:individual_url>/', individual_page, name='individual_page'),
    path('for-tech/<slug:individual_url>/', individual_page, name='individual_page'),
    path('for-clinics/<slug:individual_url>/', individual_page, name='individual_page'),
]
