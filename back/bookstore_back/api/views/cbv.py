from rest_framework.permissions import IsAuthenticated


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from django.contrib.auth.models import User
from rest_framework import viewsets

from ..filters import BookFilter
from ..models import  Book, BookImage
from ..serializers import BookSerializer, BookImageSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class BooksListAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)
    filter_class = BookFilter
    filterset_fields = ('name', 'price',)
    search_fields = ('name', 'price',)
    ordering_fields = ('name', 'price',)


class BookDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, book_id):
        book = self.get_object(book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, book_id):
        book = self.get_object(book_id)
        serializer = BookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    def delete(self, request, book_id):
        book = self.get_object(book_id)
        book.delete()
        return Response({'deleted': True})


class CategoryBooksAPIView(APIView):
    def get(self, request, category_id):
        category_books = []
        books = Book.objects.all()
        for book in books:
            if book.category.id == category_id:
                category_books.append(book)
        serializer = BookSerializer(category_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageListAPIView(APIView):
    def get(self, request):
        images = BookImage.objects.all()
        serializer = BookImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return BookImage.objects.get(id=id)
        except BookImage.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, image_id):
        image = self.get_object(image_id)
        serializer = BookSerializer(image)
        return Response(serializer.data)

    def put(self, request, image_id):
        image = self.get_object(image_id)
        serializer = BookImageSerializer(instance=image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    def delete(self, request, image_id):
        image = self.get_object(image_id)
        image.delete()
        return Response({'deleted': True})
