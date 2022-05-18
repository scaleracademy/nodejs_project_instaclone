from rest_framework import permissions


# TODO: IMPLEMENT PERMISSIONS FOR UPDATING, DELETING POSTS, LIKES AND OTHER RELEVANT OBJECTS

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # TODO: IMPLEMENT PERMISSIONS REQUIRED FOR PRIVATE PROFILES

        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = obj.author == request.user.profile

        return


class HasPostPublishingPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        # If request is to update and user does not have publishing permissions return false
        if request.method == 'PUT' and not request.user.has_perm("content.can_publish_posts"):
            return False

        return True


class IsRestrictedUser(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.groups.filter(name='restricted_access').exists():
            return False
        else:
            return True


# Admin - all groups
# Content moderator 1 - can_modify_comments
# Content moderator 2 - can_modify_comments, can_moderate_posts

# Role is define by business logic or need
# Role can consist of 1 to n groups depending on what it is supposed to do