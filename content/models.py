from django.db import models
from users.models import TimeStamp, UserProfile


# Create your models here.

class PostTagMasterList(TimeStamp):

    name = models.CharField(max_length=255)


# n number of photos or videos in a post


# 1, 2, 3
# UserPost -> PostTagMasterList
# 1 -> 5,6,7
# 2 -> 8,9,10
# 3 -> 11, 12, 13

# 1 ->5
# 1 ->6
# 1 ->7
# 2 -> 8
# 2 -> 9
# 2 -> 10

# Select ... where id in (1,2,3) => 5,6,7,8,9,10
# Joins them in python and/or in memory
# prefetch_related -> Join happens in memory after querying the db for the many to many related objects
# Without prefetch -> Every single relationship triggers a db query
# With prefetch -> We have combined all relationship queries into one

class UserPost(TimeStamp):

    caption_text = models.CharField(max_length=255, null=True)
    # TODO: STORE LAT LONG INSTEAD OF STRING
    location = models.CharField(max_length=255, null=True, db_index=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                               related_name='post')
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField(PostTagMasterList)

    class Meta:
        permissions = (
            ('can_publish_posts', 'Can Publish posts'),
        )
        indexes = [
            models.Index(fields=['location', 'created_on'], name="location_created_idx"),
            models.Index(fields=['location', '-created_on'], name="location_created_desc_idx"),
            models.Index(fields=['caption_text', '-updated_on'], name="caption_updated_idx")
        ]


class PostMedia(TimeStamp):

    def media_name(instance, filename):
        ext = filename.split(".")[-1]

        # TODO: IMPLEMENT A UUID instead of integer post id

        return f'post_media/{instance.post.id}_{instance.sequence_index}.{ext}'

    # TODO: LIMIT THIS FIELD TO ACCEPT FILES OF A CERTAIN TYPE AND SIZE - Hint: validator attribute

    media_file = models.FileField(upload_to=media_name)
    sequence_index = models.PositiveSmallIntegerField(default=0)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE,
                              related_name='media')

    class Meta:
        unique_together = ('sequence_index', 'post', )

# TODO: IMPLEMENT REACTIONS INSTEAD OF LIKES
class PostLikes(TimeStamp):

    post = models.ForeignKey(UserPost, on_delete=models.CASCADE,
                             related_name='likes')

    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                 related_name='liked_posts')

    class Meta:
        unique_together = ('post', 'liked_by', )

# TODO: IMPLEMENT NESTED COMMENTS
# TODO: IMPLEMENT LIKES ON COMMENTS
#
# GET - /resource/<resource_id>- DETAIL/retreive
# GET - /resource/  - List


class PostComments(TimeStamp):

    post = models.ForeignKey(UserPost, on_delete=models.CASCADE,
                             related_name='comments')

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                               related_name='comments_made')

    text = models.CharField(max_length=255)



   # indexes = [
   #          models.Index(fields=['last_name', 'first_name']),
   #      ]
