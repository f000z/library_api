from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import Books
from .serializers import BookSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model

from .serializers import UserSerializers


class BookListApi(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


@api_view(['GET'])
def book_list_view(request, *args, **kwargs):
    books = Books.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


class BookDetailView(generics.RetrieveAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookDeleteApiView(generics.DestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookUpdateApiView(generics.UpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class CreateApiView(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookListCreateApiView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class BookUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


from rest_framework.views import APIView


class BookListApi(APIView):
    def get(self, request):
        books = Books.objects.all()
        serializer_data = BookSerializer(books, many=True).data
        data = {
            'status': f"Returned {len(books)} books",
            'books': serializer_data
        }
        return Response(data)


class BookCreateApi(APIView):
    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': f"Books are saved to the database",
                'books': data
            }
            return Response(data)
        else:
            return Response(
                data={
                    'status': False,
                    'message': 'Serializer is not valid'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class BookDetailApi(APIView):
    def get(self, request, pk):
        try:
            book = Books.objects.get(id=pk)
            serializer_data = BookSerializer(book).data
            data = {
                'status': "Successfully",
                'book': serializer_data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                data={
                    'status': "False",
                    'message': 'Book is not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class BookDeleteApi(APIView):
    def delete(self, request, pk):
        try:
            book = Books.objects.get(id=pk)
            book.delete()
            return Response(
                data={
                    'status': True,
                    'message': 'Successfully deleted'
                },
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                data={
                    'status': False,
                    'message': 'Book is not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class BookUpdateApi(APIView):
    def put(self, request, pk):
        book = get_object_or_404(Books.objects.all(), id=pk)
        data = request.data
        serizalizer = BookSerializer(instance=book, data=data, partial=True)
        if serizalizer.is_valid(raise_exception=True):
            book_saved = serizalizer.save()
            return Response(
                data={
                    'status': True,
                    'message': f'Book {book_saved} update successfully'
                }
            )


class BookViewset(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class UserViewset(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers
