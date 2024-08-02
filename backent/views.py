from rest_framework import generics
from .models import Books
from .serializers import BookSerializers


class BookView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializers


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializers
    lookup_field = 'pk'
