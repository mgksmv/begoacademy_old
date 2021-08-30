from django.urls import path
from seminars.views import all_seminars, seminar_detail

urlpatterns = [
    path('', all_seminars, name='all_seminars'),
    path('<slug:seminar_url>/', seminar_detail, name='seminar_detail'),
    path('category/<slug:category_url>/', all_seminars, name='seminar_by_category'),
]
