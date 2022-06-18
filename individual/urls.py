from django.urls import path
from .views import ForDentistsListView, ForTechListView, ForClinicsListView, IndividualDetailView

urlpatterns = [
    path('for-dentists/', ForDentistsListView.as_view(), name='for_dentists'),
    path('for-tech/', ForTechListView.as_view(), name='for_tech'),
    path('for-clinics/', ForClinicsListView.as_view(), name='for_clinics'),
    path('for-dentists/<slug:url>/', IndividualDetailView.as_view(), name='individual_page'),
    path('for-tech/<slug:url>/', IndividualDetailView.as_view(), name='individual_page'),
    path('for-clinics/<slug:url>/', IndividualDetailView.as_view(), name='individual_page'),
]
