from django.urls import path
from .views import HomeListView, ContactsFormView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsFormView.as_view(), name='contacts'),
]
