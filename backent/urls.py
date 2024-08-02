from django.urls import path
from .views import BookView, BookDetail


urlpatterns = (
    path('book/', BookView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail')
)
