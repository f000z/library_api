from rest_framework import serializers
from .models import Books
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id', 'title', 'subtitle', 'content', 'author', 'isbn', 'price')

    def validat(self, data):
        title = data.get('title', None)
        author = data.get('author', None)

        if not title.isalpha():
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Kitob sarlovhasi faqat harflardan iborat bulishi kerak'
                }
            )

        if Books.objects.filter(title=title, author=author):
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Kitob sarlovhasi va muallifi bir xil bulgan kitobni yuklab bulmaydi'
                }
            )

    def validate_price(self, price):
        if price < 0 or price > 999999999:
            raise ValidationError(
                {
                    'status': False,
                    'message': 'Narx notugri kiritilgan qaytatdan urunib kuring'
                }
            )


class CashSerializer(serializers.Serializer):
    input = serializers.CharField(max_length=150)
    output = serializers.CharField(max_length=150)


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password')

