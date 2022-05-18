from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserPost, PostMedia, PostLikes, PostComments, PostTagMasterList
from users.serializers import UserProfileViewSerializer, UserProfileAuthorPostViewSerializer


class UserPostCreateSerializer(ModelSerializer):

    def create(self, validated_data):

        validated_data['author'] = self.context['current_user']

        return UserPost.objects.create(**validated_data)

    class Meta:
        model = UserPost
        fields = ('caption_text', 'location', 'id', 'is_published', )


class PostMediaCreateSerializer(ModelSerializer):

    class Meta:
        model = PostMedia
        fields = ('media_file', 'sequence_index', 'post')


class PostMediaViewSerializer(ModelSerializer):

    class Meta:
        model = PostMedia
        exclude = ('post', )


class PostTagViewSerializer(ModelSerializer):

    class Meta:
        model = PostTagMasterList
        fields = ('name', )


class PostFeedSerializer(ModelSerializer):

    # TODO: CREATE A SERIALIZER MORE APPROPRIATE FOR AUTHOR IN FEED
    author = serializers.SerializerMethodField()
    media = PostMediaViewSerializer(many=True)
    tags = PostTagViewSerializer(many=True)
    like_count = serializers.IntegerField()

    class Meta:
        model = UserPost
        fields = '__all__'
        include = ('media', 'like_count', )

    def get_author(self, obj):

        author_data = UserProfileAuthorPostViewSerializer(instance=obj.author).data

        author_data['follower_count'] = obj.author_follower_count
        author_data['following_count'] = obj.author_following_count

        return author_data


class PostLikeCreateSerializer(ModelSerializer):

    def create(self, validated_data):

        validated_data['liked_by'] = self.context['current_user']

        return PostLikes.objects.create(**validated_data)

    class Meta:
        model = PostLikes
        fields = ('id', 'post', )


class PostCommentCreateSerializer(ModelSerializer):

    def create(self, validated_data):

        validated_data['author'] = self.context['current_user']

        return PostComments.objects.create(**validated_data)

    class Meta:
        model = PostComments
        fields = ('id', 'text', 'post', )