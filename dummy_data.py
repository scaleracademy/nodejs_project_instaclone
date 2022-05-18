from faker import Faker
from faker.providers import profile, person, internet
from django.contrib.auth.hashers import make_password
import random

fake = Faker()

fake.add_provider(profile)
fake.add_provider(person)
fake.add_provider(internet)

from users.models import UserProfile, User, NetworkEdge
from content.models import UserPost, PostMedia, PostLikes, PostComments


def populate_users(count=1000):

    for _ in range(count):

        profile = fake.profile()

        try:
            new_user = User.objects.create(first_name=fake.first_name(),
                                           last_name=fake.last_name(),
                                           username=profile['username'],
                                           email=profile['mail'],
                                           password=make_password(profile['company']))

            UserProfile.objects.create(user=new_user,
                                       bio=profile['job'],
                                       profile_pic_url=profile['website'][0],
                                       is_verified=True)

            print("User id %d created" % new_user.id)
        except Exception as e:
            print("Some issue occurred with creating the user. Moving on to next")


def create_followers(count_of_users=100):

    ids = UserProfile.objects.all().values('id')

    for user in UserProfile.objects.all()[:count_of_users]:

        following_edges = random.randint(4, 60)

        following_edges_id = random.sample(list(ids), following_edges)

        print(following_edges_id)

        followed_by_edges = random.randint(4, 60)

        followed_by_edges_id = random.sample(list(ids), followed_by_edges)

        for to_follow in following_edges_id:

            print("To follow -> ", to_follow)

            if to_follow == user.id or \
                    NetworkEdge.objects.filter(from_user=user, to_user_id=to_follow['id']).exists():
                continue

            NetworkEdge.objects.create(from_user=user, to_user_id=to_follow['id'])

        for followed_by in followed_by_edges_id:

            print("Followed by ->", followed_by)

            if followed_by == user.id or \
                    NetworkEdge.objects.filter(to_user=user, from_user_id=followed_by['id']).exists():
                continue

            NetworkEdge.objects.create(to_user=user, from_user_id=followed_by['id'])


def create_posts(count_of_posts=1000):

    for user in UserProfile.objects.all()[:count_of_posts]:

        count_of_media = random.randint(1,4)

        post = UserPost.objects.create(caption_text=
                                       fake.profile()['job'],
                                       location=fake.city(),
                                       author=user)

        print("Post created")

        for _ in range(count_of_media):
            PostMedia.objects.create(media_file=fake.image_url(),
                                     sequence_index=_,
                                     post=post)

            print("Media created for post id %d" % post.id)