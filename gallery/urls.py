from django.urls import path
from .views import GalleryListView, GalleryDetailView

urlpatterns = [
    path('', GalleryListView.as_view(), name='gallery'),
    path('<slug:url>/', GalleryDetailView.as_view(), name='gallery_page')
]
