from rest_framework import serializers

import like
from category.models import Category
from comment.serializers import CommentSerializers
from like.models import Like
from like.serializers import LikeSerializer
from post.models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'owner_username', 'category', 'category_name', 'preview')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        comments = instance.comments.all()
        repr['comments_count'] = comments.count()
        repr['like_count'] = instance.likes.count()  # 2 способ
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = user.likes.filter(post=instance).exists()
        return repr


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    category = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Category.objects.all()
    )
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        for image in images:
            PostImage.objects.create(image=image, post=post)

        return post


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)
    comments = CommentSerializers(many=True) # Способ - related name
    # likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        comments = instance.comments.all()
        repr['comments_count'] = comments.count()
        repr['comments'] = CommentSerializers(comments, many=True).data
        repr['like_count'] = instance.likes.count() # 2 способ
        user = self.context['request'].user
        print(user)
        if user.is_authenticated:
            repr['is_liked'] = user.likes.filter(post=instance).exists()
        return repr

