from django.shortcuts import render
from .models import User, UserProfile, NetworkEdge
from .form import UserSignUpForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserProfileViewSerializer, UserProfileUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins

from .serializers import NetworkEdgeCreationSerializer, NetworkEdgeListViewSerializer, UserProfileListViewSerializer


def index(request):

    # len(User.objects.all()) => Dont do this, bad idea

    count_of_users = User.objects.count()

    users = User.objects.all()

    for user in users:
        print(user.name)


    context = {
        "count_of_users": count_of_users,
        "users": users
    }

    return render(request, 'users/index.html', context)

# GET & POST


def signup(request):

    form = UserSignUpForm()
    errors = []
    message = None

    # When the data is present to be saved
    # That is the case when the request method is of type POST
    if request.method == "POST":

        form = UserSignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            message = "New user created"
        else:
            errors = form.errors

    context = {
        'form': form,
        'errors': errors,
        'message': message

    }

    return render(request, 'users/signup.html', context)


@api_view(['POST'])
def create_user(request):

    serializer = UserCreateSerializer(data=request.data)

    response_data = {
        "errors": None,
        "data": None
    }

    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        response_data["data"] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
       }

        response_status = status.HTTP_201_CREATED
    else:
        response_data['errors'] = serializer.errors
        response_status = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=response_status)


# TODO: MOVE USER LIST API ENDPOINT TO A CLASS BASED VIEW (DEFINE A NEW ONE) - /users/list/ - try and do with ListMixin

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request):
    from django.db.models import Count
    # Protect this view

    # Better representation for user object

    users = UserProfile.objects.all().select_related('user').annotate(
        follower_count=Count('followers', distinct=True),
        following_count=Count('following', distinct=True)
    )

    serialized_data = UserProfileListViewSerializer(instance=users, many=True)

    return Response(serialized_data.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test_view(request):

    city = request.data.get('City')

    # Count of users in a certain city

    count = User.objects.filter(city=city).count()

    countof = len(User.objects.filter(city=city))

    # If a user satisfying a criteria is present or not

    # TODO: Explore performance difference between .count() and .exists()

    user = UserProfile.objects.filter(is_verified=True)

    user_count = UserProfile.objects.filter(is_verified=True).count() # if user.count()

    user_exists = UserProfile.objects.filter(is_verified=True).exists() # if user.exists()


class UserProfileDetail(APIView):

    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication, ]

    # TODO: Approach1: UPDATE THIS ENDPOINT TO RESPOND WITH A USERS POSTS ALONG WITH THE PROFILE - in this view
    # TODO: Approach2: CREATE AN ENDPOINT THAT RETURNS PUBLISHED POSTS OF A GIVEN USER - in content view

    def get(self, request, pk):

        user = UserProfile.objects.filter(id=pk).select_related('user').first()

        if user:
            serializer = UserProfileViewSerializer(instance=user)
            response_data = {
                "data": serializer.data,
                "error": None
            }
            response_status = status.HTTP_200_OK
        else:
            response_data = {
                "data": None,
                "error": "User does not exist"
            }
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response_data, status=response_status)

    def post(self, request, pk):

        user_profile_serializer = UserProfileUpdateSerializer(instance=request.user.profile,
                                                              data=request.data)
        response_data = {
            "data": None,
            "errors": None
        }

        if user_profile_serializer.is_valid():
            user_profile = user_profile_serializer.save()

            response_data['data'] = UserProfileViewSerializer(instance=user_profile).data

            response_status = status.HTTP_200_OK

        else:

            response_data['errors'] = user_profile_serializer.errors
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(response_data, response_status)

    def delete(self, request, pk):

        user = request.user

        user.delete()

        response_data = {
            "data": None,
            "message": "User object deleted successfully"
        }

        return Response(response_data, status=status.HTTP_200_OK)


# default behaviour of the mixins
# override the default behaviour of the mixins - overriding the methods such as get_queryset or get_serializer class

class UserNetworkEdgeView(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          generics.GenericAPIView):

    queryset = NetworkEdge.objects.all()
    serializer_class = NetworkEdgeCreationSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    def get_serializer_class(self):

        if self.request.method == 'GET':
            # TODO: Change the serializer in case followers are being requested
            return NetworkEdgeListViewSerializer

        return self.serializer_class

    def get_queryset(self):

        edge_direction = self.request.query_params['direction']

        # TODO: IMPROVE PERFORMANCE OF THIS ENDPOINT BY USING SELECT RELATED AND ANNOTATION
        # Hints: select related will need to be on multiple attributes
        # Do annotation to reduce the queries

        if edge_direction == 'followers':
            return self.queryset.filter(to_user=self.request.user.profile)
        elif edge_direction == 'following':
            return self.queryset.filter(from_user=self.request.user.profile)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        # TODO: IMPLEMENT THIS USING SERIALIZER CONTEXT OBJECT

        request.data['from_user'] = request.user.profile.id

        return self.create(request, *args, **kwargs)

    # car - color, manufacturer,year_of_purchase

    def delete(self, request, *args, **kwargs):

        # TOKEN WILL GIVE IDENTITY OF THE USER WHO IS TRYING TO UNFOLLOW
        # ID of the user being unfollowed can be supplied from the body
        # TODO: IMPLEMENT THIS USING THE NETWORKEDGE PK

        network_edge = NetworkEdge.objects.filter(from_user=request.user.profile,
                                                  to_user=request.data['to_user'])

        if network_edge.exists():
            network_edge.delete()
            message = "User unfollowed"
        else:
            message = "No edge found"

        return Response({"data": None, "message": message}, status=status.HTTP_200_OK)




# .select_related('from_user', 'from_user__user').annotate(
#                 follower_count=Count('from_user__followers', distinct=True),
#                 following_count=Count('from_user__following', distinct=True)
#             )

# edge_direction = self.request.query_params['direction']
#
# if edge_direction == 'followers':
#     return NetworkEdgeFollowerViewSerializer
# elif edge_direction == 'following':
#     return NetworkEdgeFollowingViewSerializer