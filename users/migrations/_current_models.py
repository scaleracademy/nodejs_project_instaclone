from django.db import models
from django.contrib.auth.models import User


class TimeStamp(models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStamp):

    # TODO: ADD VERIFICATION FOR SIZE AND TYPE OF PROFILE PIC BEING UPLOADED

    # TODO: MODIFY THE NAMING OF THE FILE BEING SAVED SO THAT THE UPDATE VIEW  BECOMES IDEMPOTENT OR COMPLIANT
    # WITH PUT REQUESTS

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False,
                                related_name='profile')
    profile_pic_url = models.ImageField(upload_to='profile_pic/', blank=True)

    bio = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=True)

# Network - edges

#   A ------> B
#   B ------> A
#   A ------> C
#   B ------> C

# user_a -> Who does user_a follow?
# NetworkEdge.objects.filter(from_user=user_a)
# user_a.following.all()  -> [B,C] -> TWO EDGES
# user_a.followers.

# user_b

# TODO: CREATE A SYSTEM FOR PRIVATE PROFILES WHERE USERS CAN DECIDE WHO IS FOLLOWING THEM

class NetworkEdge(TimeStamp):

    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                  related_name="following")

    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                related_name="followers")

    class Meta:
        unique_together = ('from_user', 'to_user',)