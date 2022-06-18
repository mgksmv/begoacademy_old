from django.urls import path
from seminars.views import SeminarsListView, SeminarDetailView

urlpatterns = [
    path('', SeminarsListView.as_view(), name='all_seminars'),
    path('<slug:url>/', SeminarDetailView.as_view(), name='seminar_detail'),
    path('category/<slug:category_url>/', SeminarsListView.as_view(), name='seminar_by_category'),
]
