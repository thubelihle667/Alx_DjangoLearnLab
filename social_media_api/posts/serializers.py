from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "author", "title", "content",
            "created_at", "updated_at",
            "comment_count",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at", "comment_count"]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Content must be at least 5 characters.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    post_id = serializers.PrimaryKeyRelatedField(
        source="post", queryset=Post.objects.all(), write_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id", "post_id", "author", "content",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be blank.")
        return value
