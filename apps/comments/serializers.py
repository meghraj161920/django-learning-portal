from rest_framework import serializers
from .models import Comment, CommentUpvote
from apps.accounts.serializers import PublicProfileSerializer


class ReplySerializer(serializers.ModelSerializer):
    author = PublicProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'content',
            'upvotes',
            'created_at',
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = PublicProfileSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    reply_count = serializers.IntegerField(
        source='replies.count',
        read_only=True
    )
    has_upvoted = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'content',
            'upvotes',
            'reply_count',
            'replies',
            'has_upvoted',
            'created_at',
            'updated_at',
        ]

    def get_has_upvoted(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.upvote_records.filter(
                user=request.user
            ).exists()

        return False


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'lesson',
            'parent',
            'content',
        ]

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)