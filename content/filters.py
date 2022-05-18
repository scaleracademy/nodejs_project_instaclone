from rest_framework import filters


class CurrentUserFollowingFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        # Gives me a list of all users being followed by the current user
        followed_users = [edge.to_user for edge in request.user.profile.following.all()]

        return queryset.filter(author__in=followed_users,
                                is_published=True)