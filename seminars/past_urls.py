from django.urls import path
from seminars.views import SeminarsListView

urlpatterns = [
    path('', SeminarsListView.as_view(), name='past_seminars'),
    path('category/<slug:category_url>/', SeminarsListView.as_view(), name='past_seminar_by_category'),
]
