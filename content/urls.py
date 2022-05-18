from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('like', views.PostLikeViewSet)
router.register('comment', views.PostCommentViewSet)

# GET /resource/  but no path param - list
# GET /resource/ with path param - retreive
# POST /resource/ - create
# PUT - needs path param to work - update
# PATCH - needs path param to work - partial_update
# DELETE - needs path param to work - Delete

#Create a post/Update a post
# Upload media
# View the post - feed, postdetail

# Every image/video is uploaded individually using the upload media endpoints
# The post object is create with no media/caption because it is needed as reference
# GET - /post/

urlpatterns = [
    path('', views.UserPostCreateFeed.as_view(), name='user_post_view'),
    path('media/', views.PostMediaView.as_view(), name='post_media_view'),
    path('<int:pk>/', views.UserPostDetailUpdateView.as_view(), name='post_detail_update'),
    path('', include(router.urls))
]