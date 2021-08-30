from django.urls import path
from seminars.views import past_seminars, seminar_detail

urlpatterns = [
    path('', past_seminars, name='past_seminars'),
    path('<slug:seminar_url>/', seminar_detail, name='past_seminar_detail'),
    path('category/<slug:category_url>/', past_seminars, name='past_seminar_by_category'),
]
