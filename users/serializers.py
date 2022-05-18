from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, NetworkEdge
from django.contrib.auth.hashers import make_password


class UserCreateSerializer(ModelSerializer):

    def create(self, validate_data):

        validate_data['password'] = make_password(validate_data['password'])

        user = User.objects.create(**validate_data)

        UserProfile.objects.create(user=user)

        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'email', )


class UserViewSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', )


class UserProfileAuthorPostViewSerializer(ModelSerializer):

    user = UserViewSerializer()

    class Meta:
        model = UserProfile
        fields = ('profile_pic_url', 'bio', 'user', )


class UserProfileViewSerializer(ModelSerializer):

    user = UserViewSerializer()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ('id', 'is_verified', )

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class UserProfileListViewSerializer(ModelSerializer):

    user = UserViewSerializer()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ('id', 'is_verified', )

    def get_follower_count(self, obj):
        return obj.follower_count

    def get_following_count(self, obj):
        return obj.following_count


class UserProfileUpdateSerializer(ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def update(self, instance, validated_data):

        user = instance.user

        user.first_name = validated_data.pop('first_name', None)
        user.last_name = validated_data.pop('last_name', None)

        user.save()

        instance.bio = validated_data.get('bio', None)
        instance.profile_pic_url = validated_data.get('profile_pic_url', None)
        instance.save()

        return instance

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'bio', 'profile_pic_url', )


class NetworkEdgeCreationSerializer(ModelSerializer):

    class Meta:
        model = NetworkEdge
        fields = ('from_user', 'to_user', )


class NetworkEdgeListViewSerializer(ModelSerializer):

    # TODO: DEFINE A NEW SERIALIZER THAT CONTAINS FIELDS RELEVANT TO THE FOLLOWER COUNT OR FOLLOWING COUNT VIEW
    # TODO: INCLUDE THE ID OF THE to_user

    from_user = UserProfileViewSerializer()

    class Meta:
        model = NetworkEdge
        fields = ('from_user', )











# class NetworkEdgeFollowerViewSerializer(ModelSerializer):
#
#
#
#     #from_user = UserProfileViewSerializer()
#     from_user = serializers.SerializerMethodField()
#
#     class Meta:
#         model = NetworkEdge
#         fields = ('from_user', )

    # def get_from_user(self, obj):
    #     data = NetworkEdgeUserProfileViewSerializer(instance=obj.from_user).data
    #     data['follower_count'] = obj.follower_count
    #     data['following_count'] = obj.following_count
    #
    #     print(data)
    #     return data


# class NetworkEdgeFollowingViewSerializer(ModelSerializer):
#
#     # TODO: DEFINE A NEW SERIALIZER THAT CONTAINS FIELDS RELEVANT TO THE FOLLOWER COUNT OR FOLLOWING COUNT VIEW
#     # TODO: INCLUDE THE ID OF THE to_user
#
#     to_user = UserProfileViewSerializer()
#
#     class Meta:
#         model = NetworkEdge
#         fields = ('to_user', )


# class NetworkEdgeUserProfileViewSerializer(ModelSerializer):
#
#     user = UserViewSerializer()
#
#     class Meta:
#         model = UserProfile
#         exclude = ('id', 'is_verified', )