from django.urls import path
from .views import LectorsListView, LectorDetailView

urlpatterns = [
    path('', LectorsListView.as_view(), name='lectors'),
    path('<slug:url>', LectorDetailView.as_view(), name='lector_page')
]
