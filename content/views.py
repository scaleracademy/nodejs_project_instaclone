from django.shortcuts import render

from django.db.models import Count
from .models import UserPost, PostLikes, PostComments
from .serializers import UserPostCreateSerializer, \
    PostMediaCreateSerializer, PostFeedSerializer, PostLikeCreateSerializer, PostCommentCreateSerializer
from .filters import CurrentUserFollowingFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets

from .permissions import IsOwnerOrReadOnly, HasPostPublishingPermission


from .tasks import process_media


# Create your views here.

# Post creation flow

# create post with just the author id
# upload media files with the reference of post id obtained in the last step
# update the post and publish

# Permission or group creation - django creates 4 permissions by default for every model
# Permission check - add a check as and where required - has_perm()
# Permission or group grant - give a user a certain permission - 1) Code 2) Admin

class UserPostCreateFeed(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         generics.GenericAPIView):

    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializer
    #filter_backends = [CurrentUserFollowingFilterBackend, ]

    # TODO: CREATE A SYSTEM TO FOLLOW TOPICS OR HASHTAGS
    # TODO: CREATE A WAY OR ORDERING THE FEED - BASED ON POST POPULARITY

    def get_queryset(self):
        queryset = self.queryset.select_related('author', 'author__user')

        queryset = queryset.prefetch_related('tags', 'media')

        queryset = queryset.annotate(author_follower_count=Count('author__followers', distinct=True))

        queryset = queryset.annotate(author_following_count=Count('author__following', distinct=True))

        queryset = queryset.annotate(like_count=Count('likes', distinct=True))

        return queryset

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return PostFeedSerializer

        return self.serializer_class

    def post(self, request, *args, **kwargs):

        response = self.create(request, *args, **kwargs)

        return response

    def get(self, request, *args, **kwargs):
        # UserPost.objects.filter(is_published=True, author__in = followers_of_current_user)
        # Select * from content_post where author_id__in (1,2,3) ;
        return self.list(request, *args, **kwargs)


class PostMediaView(mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = PostMediaCreateSerializer

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

from datetime import datetime
class UserPostDetailUpdateView(mixins.UpdateModelMixin,
                               mixins.RetrieveModelMixin,
                               generics.GenericAPIView):
    # TODO: CREATE A CELERY TASK THAT CAN PROCESS IMAGES TO DIFFERENT SIZES

    permission_classes = [IsAuthenticated, HasPostPublishingPermission]
    authentication_classes = [JWTAuthentication, ]
    serializer_class = UserPostCreateSerializer
    queryset = UserPost.objects.all()

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return PostFeedSerializer

        return self.serializer_class

    def put(self, request, *args, **kwargs):

        response = self.update(request, *args, **kwargs)
        # process_media.delay(post_id) # Figure out where the post_id can be accessed from
        # a.delay()
        # b.delay()
        # c.delay()

        return response

    # TODO: FILTER OUT POSTS THAT ARE NOT PUBLISHED YET
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # TODO: CREATE AN ENDPOINT TO DELETE A POST


from rest_framework.response import Response

# Viewset - urls get configured automatically but
    # the methods need to be implemented for the HTTP verbs to work

# GENERICViewset - add mixins
    # also has methods such as get_serializer_class, get_queryset etc available for override

# ModelViewSet - urls + methods are implemented


class PostLikeViewSet(
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]
    queryset = PostLikes.objects.all()
    serializer_class = PostLikeCreateSerializer

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    # TODO: IMPLEMENT get_serializer_class method and an appropriate serializer for the like list
    # TODO: Update post listing/feed serializers to carry the like count
    # TODO: Update post listing/feed serializer to show usernames of users that the current user is following
    #   who have liked a particular post

    # TODO: CREATE A NOTIFICATION SYSTEM TO NOTIFY USERS WHEN POST IS LIKED

    def list(self, request):

        post_likes = self.queryset.filter(post_id=request.query_params['post_id'])

        page = self.paginate_queryset(post_likes)

        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(post_likes, many=True)

        return Response(serializer.data)


# TODO: Update post list/feed to show the first few comments - decide on which ones to show
# TODO: CREATE A NOTIFICATION SYSTEM TO NOTIFY USERS WHEN POST IS COMMENTED ON

class PostCommentViewSet(
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, ]
    authentication_classes = [JWTAuthentication, ]
    queryset = PostComments.objects.all()
    serializer_class = PostCommentCreateSerializer

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def list(self, request):
        # TODO: SEE IF LIST METHOD FOR LIKE AND COMMENT CAN BE COMBINED
        # TODO: Implement get_serializer_class to have an appropriate response containing the user's profile

        post_comments = self.queryset.filter(post_id=request.query_params['post_id'])

        page = self.paginate_queryset(post_comments)

        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(post_comments, many=True)

        return Response(serializer.data)







# User sign up -> Send email

# A user being followed -> Send notification (email, push)

# A like -> Send notification (email, push)

# Comment -> Review the comment for foul/bad language

# A post being uploaded -> Create multiple versions of the image/video file for different sizes


# 1. You are increasing the response time for a task that is additional
# 2. You are increasing the potential risk of the API call failing


# Async








