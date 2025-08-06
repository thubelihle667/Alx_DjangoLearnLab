from rest_framewrok import serializers
from .models import Author,Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title','publication_year','author']

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='author.username', read_only=True)
    book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'book']

    def validate(self, data):
        if publication_year > 2025:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return data