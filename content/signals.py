from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PostMedia, UserPost, PostComments
from .tasks import process_media, make_media_versions


# TODO: Implement these signals

@receiver(post_save, sender=PostMedia)
def process_media(sender, instance, **kwargs):
    print("Inside post process media signal")


@receiver(post_save, sender=UserPost)
def send_new_post_notification(sender, instance, **kwargs):
    make_media_versions.delay(instance.id)
    if instance.is_published:
        print("Going to send some notifications to followers")
    else:
        print("Not going to send any notifications as post is not published")


@receiver(post_save, sender=PostComments)
def profanity_filter(sender, instance, **kwargs):
    print("Going to review comments for profanities")


@receiver(post_save, sender=PostComments)
def send_notification(sender, instance, **kwargs):
    # TODO: ADD CHECK SO THAT NOTIFICATIONS ARE NOT SENT WHEN A COMMENT IS UPDATED
    print("Going to notify a user that comment has been made on their post")